from ...algorithms.cascades.tools import (skipEmptyRectangles, isRectangle, loadScript)
from ...algorithms.cascades.scripts_detectors import RotatedCascadesDetector
from handling import load_temp_data, save_temp_data, remove_temp_data
from ..general.process_interface import AlgorithmProcessInterface
from ...algorithms.cvtools import numpy_ndarrayToList, rotate90
from ...algorithms.cascades import SCRIPTS_PATH
from ..helpers import partial_results_handler
from defs import STATUS_ERROR, STATUS_RESULT
from settings.settings import get_settings
import os


ROTATION_DETECTION_PROCESS_CLASS_NAME = "RotationDetectionProcess"


def job(callback_code, **kwargs):
    RotationDetectionProcess.job(callback_code, **kwargs)


class RotationDetectionProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)
        self._classname = ROTATION_DETECTION_PROCESS_CLASS_NAME
        self._r_result_process = AlgorithmProcessInterface()

    def set_rotation_result_process(self, process):
        self._r_result_process = process

    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary:
            {
                'status': 'result',
                'data':
                {
                    'data_list': string dict list
                        [
                            "{'data_file': data file path}",
                            "{'data_file': data file path}",
                            "{'data_file': data file path}",
                            "{'data_file': data file path}"
                        ]
                },
                'type': 'detection'
            }
        """
        self._handler_logger_info(result)
        if result is not None:
            if result['status'] == STATUS_ERROR:
                pass
            elif result['status'] == STATUS_RESULT:
                self._r_result_process.run(self._worker, **result['data'])

    @staticmethod
    def job(callback_code, **kwargs):
        """
        Job function for rotation detecting.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'data_file': data file path,
                'angle': angle key value
            }
        """
        RotationDetectionProcess._job_logger_info(ROTATION_DETECTION_PROCESS_CLASS_NAME, **kwargs)
        record = {'data_file': RotationDetectionProcess.process(**kwargs)}
        if partial_results_handler(callback_code, record):
            remove_temp_data(kwargs['data_file'])

    @staticmethod
    def process(**kwargs):
        RotationDetectionProcess._process_logger_info(ROTATION_DETECTION_PROCESS_CLASS_NAME, **kwargs)
        source = load_temp_data(kwargs['data_file'], remove=False)
        settings = get_settings(source['algoID'])
        img = source['data']
        for i in range(0, kwargs["angle"], 1):
            img = rotate90(img)
        rects = []
        d = dict()
        rotation_script_dict = loadScript(os.path.join(SCRIPTS_PATH, settings['rotation_script']))
        rotation_script = RotatedCascadesDetector.init_stage(rotation_script_dict)
        detector = RotatedCascadesDetector(rotation_script_dict, dict())
        if len(rotation_script.stages) > 1:
            r = []
            for stage in rotation_script.stages:
                lr1 = detector.apply_stage(img, stage)
                r += lr1
                for lr in lr1:
                    d[str(lr)] = kwargs["angle"] + 1
            if isRectangle(r[0]):
                rects = skipEmptyRectangles(r)
        else:
            stage = rotation_script.stages[0]
            r1 = detector.apply_stage(img, stage)
            rects += r1
            for lr in r1:
                d[str(lr)] = kwargs["angle"] + 1
            rects = skipEmptyRectangles(rects)
        source['data'] = img
        source['data_angle'] = kwargs["angle"] + 1
        source['roi_rects'] = [numpy_ndarrayToList(r) for r in rects]
        source['datagram'] = d
        temp_data_path = source['temp_data_path']
        training_process_data = save_temp_data(source, temp_data_path, ['data'])
        return training_process_data

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        # kwargs.update({'timeout': 300})
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
