from biomio.algorithms.processes.general.process_interface import AlgorithmProcessInterface
from decorators import handler_header, job_header, store_job_result


def job(callback_code, **kwargs):
    CallbackProcess.job(callback_code, **kwargs)


class CallbackProcess(AlgorithmProcessInterface):
    def __init__(self, callback):
        AlgorithmProcessInterface.__init__(self)
        self.external_callback(callback)

    @handler_header
    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary
        """
        self._callback(result)

    @classmethod
    @store_job_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        return kwargs

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
