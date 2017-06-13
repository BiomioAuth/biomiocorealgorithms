from ..general.decorators import job_header, process_header, store_partial_result
from ...algorithms.cascades.script_cascade_detector import ScriptCascadeDetector
from ..general.process_interface import AlgorithmProcessInterface
from ...algorithms.cascades.tools import loadScript
from ...algorithm_storage import AlgorithmStorage
from . import SCRIPT_CASCADE_FACE_DETECTOR


DETECTION_SCRIPT = "main_haarcascade_face_size.json"


def job(callback_code, **kwargs):
    CascadeDetectionPrepareProcess.job(callback_code, **kwargs)


class CascadeDetectionPrepareProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        if not AlgorithmStorage.instance().exists(SCRIPT_CASCADE_FACE_DETECTOR):
            AlgorithmStorage.instance().register(SCRIPT_CASCADE_FACE_DETECTOR,
                                                 ScriptCascadeDetector(loadScript("main_haarcascade_face_size.json",
                                                                                  True)))

    @classmethod
    @job_header
    @store_partial_result
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        record = CascadeDetectionPrepareProcess.process(**kwargs)
        return CascadeDetectionPrepareProcess.create_result_message(record)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        task = kwargs['task']
        detector = AlgorithmStorage.instance().get(SCRIPT_CASCADE_FACE_DETECTOR)
        if detector is not None and task is not None:
            kwargs['task_result'] = detector.apply_task(kwargs['data'], task)
        return kwargs

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
