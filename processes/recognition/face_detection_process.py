from ...algorithms.cascades.classifiers import (CascadeROIDetector, RectsFiltering, CascadeClassifierSettings)
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from ...algorithms.cascades.scripts_detectors import CascadesDetectionInterface
from ...algorithms.cascades import SCRIPTS_PATH, CASCADES_PATH, mergeRectangles
from ..general.decorators import process_header, handler_header, job_header
from ..general.process_interface import AlgorithmProcessInterface, logger
from defs import STATUS_ERROR, STATUS_RESULT, INTERNAL_TRAINING_ERROR
from ...algorithms.cascades.tools import loadScript, getROIImage
from messages import create_error_message, create_result_message
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from handling import load_temp_data, save_temp_data
from settings.settings import get_settings
import os


def job(callback_code, **kwargs):
    FaceDetectionProcess.job(callback_code, **kwargs)


class FaceDetectionProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)
        self._next_process = AlgorithmProcessInterface()

    def set_next_process(self, process):
        self._next_process = process

    @handler_header
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
        if result is not None:
            if result['status'] == STATUS_ERROR:
                pass
            elif result['status'] == STATUS_RESULT:
                self._next_process.run(self._worker, **result['data'])

    @classmethod
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for handling rotation results.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                "{'data_file': data file path}"
            }
        """
        record = FaceDetectionProcess.process(**kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        data_dict = load_temp_data(kwargs['data_file'], remove=True)
        if data_dict is not None:
            settings = get_settings(data_dict['algoID'])

            detector = CascadesDetectionInterface(loadScript(os.path.join(SCRIPTS_PATH, settings['detect_script'])))
            img, rects = detector.detect(data_dict['data'])
            optimal_rect = mergeRectangles(rects)
            if len(optimal_rect) != 4:
                face_classifier = CascadeROIDetector()
                settings = CascadeClassifierSettings()
                settings.minNeighbors = 1
                settings.minSize = (100, 100)
                face_classifier.classifierSettings = settings
                face_classifier.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt.xml"))
                face_classifier.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt_tree.xml"))
                face_classifier.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt2.xml"))
                face_classifier.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_default.xml"))
                optimal_rect = face_classifier.detectAndJoin(data_dict['data'], RectsFiltering)
            data_dict['roi'] = getROIImage(data_dict['data'], optimal_rect)
            temp_data_path = data_dict['temp_data_path']
            detection_process_data = save_temp_data(data_dict, temp_data_path, ['data', 'roi'])
            record = create_result_message({'data_file': detection_process_data}, 'detection')
        else:
            record = create_error_message(INTERNAL_TRAINING_ERROR, "data_list", "Empty list of data.")
        return record

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
