from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_PARTIAL_RESULTS_KEY, REDIS_RESULTS_COUNTER_KEY, REDIS_DO_NOT_STORE_RESULT_KEY
from biomio.algorithms.cascades.scripts_detectors import CascadesDetectionInterface, RotatedCascadesDetector
from biomio.algorithms.cascades.tools import (skipEmptyRectangles, isRectangle, loadScript)
from biomio.algorithms.recognition.processes.settings.settings import get_settings
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from defs import STATUS_ERROR, STATUS_RESULT, INTERNAL_TRAINING_ERROR
from messages import create_error_message, create_result_message
from biomio.algorithms.cvtools import numpy_ndarrayToList
from biomio.algorithms.cvtools.effects import rotate90
from biomio.algorithms.cascades import SCRIPTS_PATH
from handling import load_temp_data, save_temp_data
import os


ROTATION_DETECTION_PROCESS_CLASS_NAME = "RotationDetectionProcess"

def job(callback_code, **kwargs):
    RotationDetectionProcess.job(callback_code, **kwargs)


def store_verification_results(result, callback_code):
    AlgorithmsDataStore.instance().delete_data(key=REDIS_RESULTS_COUNTER_KEY % callback_code)
    AlgorithmsDataStore.instance().delete_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
    AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                    record_dict=result, callback_code=callback_code)


class RotationDetectionProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path):
        AlgorithmProcessInterface.__init__(self, temp_data_path)
        self._classname = ROTATION_DETECTION_PROCESS_CLASS_NAME
        self._r_result_process = AlgorithmProcessInterface()

    def set_rotation_result_process(self, process):
        self._r_result_process = process

    def handler(self, result):
        self._handler_logger_info(result)
        if result is not None:
            if result['status'] == STATUS_ERROR:
                pass
            elif result['status'] == STATUS_RESULT:
                self._r_result_process.run(self._worker, **result['data'])

    @staticmethod
    def job(callback_code, **kwargs):
        RotationDetectionProcess._job_logger_info(ROTATION_DETECTION_PROCESS_CLASS_NAME, **kwargs)
        record = {'data_file': RotationDetectionProcess.process(**kwargs)}
        AlgorithmsDataStore.instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                            value=record)
        results_counter = AlgorithmsDataStore.instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                             callback_code)
        if results_counter <= 0:
            gathered_results = AlgorithmsDataStore.instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                              callback_code)
            if results_counter < 0:
                result = create_error_message(INTERNAL_TRAINING_ERROR, "jobs_counter", "Number of jobs is incorrect.")
            else:
                result = create_result_message({'data_list': gathered_results}, 'detection')
            store_verification_results(result=result, callback_code=callback_code)

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
        rotation_script = CascadesDetectionInterface.init_stage(rotation_script_dict)
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
        temp_data_path = kwargs['temp_data_path']
        training_process_data = save_temp_data(source, temp_data_path, ['data'])
        return training_process_data

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
