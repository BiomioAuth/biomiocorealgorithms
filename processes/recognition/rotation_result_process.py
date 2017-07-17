from ...algorithms.cascades.scripts_detectors import CascadesDetectionInterface
from ..general.decorators import job_header, process_header, store_job_result
from ..messages import create_error_message, create_result_message
from ..general.process_interface import AlgorithmProcessInterface
from ..general.handling import load_temp_data, save_temp_data
from ...algorithms.cvtools.types import listToNumpy_ndarray
from ...algorithms.cascades.tools import loadScript
from ..general.defs import INTERNAL_TRAINING_ERROR
from ...algorithms.cascades import SCRIPTS_PATH
from settings.settings import get_settings
import ast
import os


def job(callback_code, **kwargs):
    RotationResultProcess.job(callback_code, **kwargs)


class RotationResultProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)

    @classmethod
    @store_job_result
    @job_header
    def job(cls, callback_code, **kwargs):
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
        kwargs['data_list'] = [ast.literal_eval(dict_str) for dict_str in kwargs['data_list']]
        return RotationResultProcess.process(**kwargs)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        images_res_list = kwargs['data_list']
        if len(images_res_list) > 0:
            data_list = [load_temp_data(im_res['data_file'], remove=True) for im_res in images_res_list]
            result = {"name": data_list[0]["name"], "path": data_list[0]["path"], 'algoID': data_list[0]['algoID'],
                      'general_data': data_list[0]['general_data'], 'temp_data_path': data_list[0]['temp_data_path']}
            if 'userID' in data_list[0]:
                result["userID"] = data_list[0]['userID']
            if 'providerID' in data_list[0]:
                result["providerID"] = data_list[0]['providerID']
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
