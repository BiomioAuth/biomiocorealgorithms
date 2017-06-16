from ..general.decorators import job_header, process_header, store_partial_result
from defs import SCRIPT_CASCADE_FACE_DETECTOR_LOADED, create_cascade_detector
from ...algorithms.cascades.script_cascade_detector import ScriptTask
from ..general.process_interface import AlgorithmProcessInterface
from ...algorithm_storage import AlgorithmStorage
from ..general.handling import serialize_database
import cv2


def job(callback_code, **kwargs):
    process = CascadeDetectionPrepareProcess(None)
    CascadeDetectionPrepareProcess.job(callback_code, **kwargs)


class CascadeDetectionPrepareProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        if not AlgorithmStorage.instance().exists(SCRIPT_CASCADE_FACE_DETECTOR_LOADED):
            AlgorithmStorage.instance().register(SCRIPT_CASCADE_FACE_DETECTOR_LOADED, create_cascade_detector(True))

    @classmethod
    @store_partial_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        return CascadeDetectionPrepareProcess.process(**kwargs)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        task = ScriptTask.parse(kwargs['task'])
        detector = AlgorithmStorage.instance().get(SCRIPT_CASCADE_FACE_DETECTOR_LOADED)
        preload_task = detector.get_tasks().get(task.name)
        if preload_task is not None:
            task = preload_task
        if detector is not None and task is not None:
            kwargs['task_result'] = serialize_database(detector.apply_task(cv2.imread(kwargs['data']), task))
        return kwargs

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
