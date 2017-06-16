import ast
import os

from biomio.algorithms.processes.general.defs import STATUS_ERROR, STATUS_RESULT, INTERNAL_TRAINING_ERROR
from ..general.handling import load_temp_data, save_temp_data
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from messages import create_error_message, create_result_message
from settings.settings import get_settings
from ..general.process_interface import AlgorithmProcessInterface
from ...algorithms.cascades import SCRIPTS_PATH
from ...algorithms.cascades.scripts_detectors import CascadesDetectionInterface
from ...algorithms.cascades.tools import loadScript
from ...algorithms.cvtools.types import listToNumpy_ndarray

ROTATION_RESULT_PROCESS_CLASS_NAME = "RotationResultProcess"


def job(callback_code, **kwargs):
    RotationResultProcess.job(callback_code, **kwargs)


class RotationResultProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)
        self._classname = ROTATION_RESULT_PROCESS_CLASS_NAME
        self._data_detect_process = AlgorithmProcessInterface()

    def set_data_detection_process(self, process):
        self._data_detect_process = process

    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary:
            {
                'status': 'result',
                'data':
                {
                    'data_file': data file path
                },
                'type': 'detection'
            }
        """
        self._handler_logger_info(result)
        if result is not None:
            if result['status'] == STATUS_ERROR:
                pass
            elif result['status'] == STATUS_RESULT:
                self._data_detect_process.run(self._worker, **result['data'])

    @staticmethod
    def job(callback_code, **kwargs):
        """
        Job function for handling rotation results.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'data_list': string dict list
                    [
                        "{'data_file': data file path}",
                        "{'data_file': data file path}",
                        "{'data_file': data file path}",
                        "{'data_file': data file path}"
                    ]
            }
        """
        RotationResultProcess._job_logger_info(ROTATION_RESULT_PROCESS_CLASS_NAME, **kwargs)
        images_res_list = [ast.literal_eval(dict_str) for dict_str in kwargs['data_list']]
        kwargs['data_list'] = images_res_list
        record = RotationResultProcess.process(**kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        RotationResultProcess._process_logger_info(ROTATION_RESULT_PROCESS_CLASS_NAME, **kwargs)
        images_res_list = kwargs['data_list']
        if len(images_res_list) > 0:
            data_list = [load_temp_data(im_res['data_file'], remove=True) for im_res in images_res_list]
            result = dict()
            result["name"] = data_list[0]["name"]
            result["path"] = data_list[0]["path"]
            result['algoID'] = data_list[0]['algoID']
            if 'userID' in data_list[0]:
                result["userID"] = data_list[0]['userID']
            if 'providerID' in data_list[0]:
                result["providerID"] = data_list[0]['providerID']
            result['general_data'] = data_list[0]['general_data']
            result['temp_data_path'] = data_list[0]['temp_data_path']
            settings = get_settings(result['algoID'])
            images = dict()
            datagram = dict()
            rects = []
            for res in data_list:
                images[res['data_angle']] = res['data']
                for ki, di in res['datagram'].iteritems():
                    datagram[ki] = di
                for rect in res['roi_rects']:
                    rects.append(rect)
            datagram[str([])] = 1
            rotation_script_dict = loadScript(os.path.join(SCRIPTS_PATH, settings['rotation_script']))
            rotation_script = CascadesDetectionInterface.init_stage(rotation_script_dict)
            rect = rotation_script.strategy.apply(rects)
            count = {1: 0, 2: 0, 3: 0, 4: 0}
            gl = {1: [0, 0, 0, 0], 2: [0, 0, 0, 0], 3: [0, 0, 0, 0], 4: [0, 0, 0, 0]}
            for rs in rect:
                if len(rs) < 1:
                    continue
                count[datagram[str(listToNumpy_ndarray(rs[1]))]] += 1
                if ((gl[datagram[str(listToNumpy_ndarray(rs[1]))]][2] < rs[0][2]) and
                        (gl[datagram[str(listToNumpy_ndarray(rs[1]))]][3] < rs[0][3])):
                    gl[datagram[str(listToNumpy_ndarray(rs[1]))]] = rs[0]
            max_count = -1
            midx = 0
            for index in range(1, 5, 1):
                if count[index] > max_count:
                    max_count = count[index]
                    midx = index
                elif count[index] == max_count:
                    if gl[index][2] > gl[midx][2] and gl[index][3] > gl[midx][3]:
                        midx = index
            result['data'] = images[midx]
            temp_data_path = result['temp_data_path']
            detection_process_data = save_temp_data(result, temp_data_path, ['data'])
            record = create_result_message({'data_file': detection_process_data}, 'detection')
        else:
            record = create_error_message(INTERNAL_TRAINING_ERROR, "data_list", "Empty list of data.")
        return record

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        # kwargs.update({'timeout': 300})
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
