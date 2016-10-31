from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY

TRANSFER_DATA_PROCESS_CLASS_NAME = "TransferDataProcess"

def job(callback_code, **kwargs):
    """
      External method for calling TransferDataProcess.job function
    from WorkerInterface.

    :param callback_code: callback function identifier
    :param kwargs: settings dictionary
    """
    TransferDataProcess.job(callback_code, **kwargs)


class TransferDataProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        """
          Initialize TransferDataProcess object and set worker for
        internal job running.

        :param worker: WorkerInterface instance
        """
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = TRANSFER_DATA_PROCESS_CLASS_NAME
        self._processes = []

    def add_transfer_process(self, process):
        """
          Add process to process list for data transfer.

        :param process: AlgorithmProcessInterface-based process instance
        """
        self._processes.append(process)

    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary (process only transfer data to other processes,
            so it can use any dictionary structure)
        """
        self._handler_logger_info(result)
        if result is not None:
            for process in self._processes:
                process.run(worker=self._worker, **result)

    @staticmethod
    def job(callback_code, **kwargs):
        """
        Job function for transfer data to few independent parallel processes.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary (process only transfer data to other processes,
            so it can use any dictionary structure)
        """
        TransferDataProcess._job_logger_info(TRANSFER_DATA_PROCESS_CLASS_NAME, **kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=kwargs, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        """
          Method for handle worker-independent process functionality.
        :param kwargs: settings dictionary
        """
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        """
          Method for run default TransferDataProcess behavior.

        :param worker: WorkerInterface instance
        :param kwargs_list_for_results_gatherer: list of kwargs dicts that will be
        given to each job one by one
        :param kwargs: settings arguments for job running
        """
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
