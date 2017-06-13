from ..general.process_interface import AlgorithmProcessInterface, RTYPE_JOB_LIST
from ...algorithms.cascades.script_cascade_detector import ScriptCascadeDetector
from ..general.decorators import job_header, process_header, store_job_result
from ...algorithms.cascades.tools import loadScript
from ...algorithm_storage import AlgorithmStorage
from . import SCRIPT_CASCADE_FACE_DETECTOR


DETECTION_SCRIPT = "main_haarcascade_face_size.json"


def job(callback_code, **kwargs):
    CascadeDetectionInitialProcess.job(callback_code, **kwargs)


class CascadeDetectionInitialProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        if not AlgorithmStorage.instance().exists(SCRIPT_CASCADE_FACE_DETECTOR):
            AlgorithmStorage.instance().register(SCRIPT_CASCADE_FACE_DETECTOR,
                                                 ScriptCascadeDetector(loadScript("main_haarcascade_face_size.json",
                                                                                  True)))

    @classmethod
    @job_header
    @store_job_result
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        record = CascadeDetectionInitialProcess.process(**kwargs)
        return CascadeDetectionInitialProcess.create_result_message(record, result_type=RTYPE_JOB_LIST)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        task_list = AlgorithmStorage.instance().get(SCRIPT_CASCADE_FACE_DETECTOR).get_tasks()
        job_list = []
        for task in task_list:
            job_list.append({'task': task})
        return [job_list, kwargs]

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
