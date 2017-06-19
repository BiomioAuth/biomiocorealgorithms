from biomio.algorithms.processes.general.decorators import job_header, store_job_result, handler_header
from biomio.algorithms.processes.general.process_interface import AlgorithmProcessInterface


def job(callback_code, **kwargs):
    PreviousSuccessProcess.job(callback_code, **kwargs)


class PreviousSuccessProcess(AlgorithmProcessInterface):
    def __init__(self, worker, active_key='data'):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._active_key = active_key
        self._alternative_process = None

    def set_alternative_handler_process(self, process):
        self._alternative_process = process

    @handler_header
    def handler(self, result):
        if result is not None:
            data = result['data']
            if data[self._active_key] is None and self._alternative_process is not None:
                self._alternative_process.run(self._worker, **data)
            else:
                self._next_process.run(self._worker, **data)

    @classmethod
    @store_job_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
            }
        """
        return PreviousSuccessProcess.create_result_message(kwargs)

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
