from ..general.process_interface import AlgorithmProcessInterface, RTYPE_JOB_LIST
from ..general.decorators import job_header, process_header, store_job_result
from defs import SCRIPT_CASCADE_FACE_DETECTOR, create_cascade_detector
from ...algorithm_storage import AlgorithmStorage


def job(callback_code, **kwargs):
    process = CascadeDetectionInitialProcess(None)
    CascadeDetectionInitialProcess.job(callback_code, **kwargs)


class CascadeDetectionInitialProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        if not AlgorithmStorage.instance().exists(SCRIPT_CASCADE_FACE_DETECTOR):
            AlgorithmStorage.instance().register(SCRIPT_CASCADE_FACE_DETECTOR, create_cascade_detector())

    @classmethod
    @store_job_result
    @job_header
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
        task_dict = AlgorithmStorage.instance().get(SCRIPT_CASCADE_FACE_DETECTOR).get_tasks()
        job_list = []
        for key, task in task_dict.iteritems():
            job_list.append({'task': task.serialize()})
        return [job_list, kwargs]

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
