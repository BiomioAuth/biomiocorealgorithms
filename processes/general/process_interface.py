from defs import STATUS_ERROR, STATUS_RESULT, RTYPE_JOB_LIST
from decorators import handler_header
from ...logger import logger


class AlgorithmProcessInterface:
    def __init__(self, temp_data_path='', worker=None):
        self._temp_data_path = temp_data_path
        self._worker = worker
        self._classname = "AlgorithmProcessInterface"
        self._error_process = None
        self._next_process = None
        self._callback = None

    def set_next_process(self, process):
        self._next_process = process

    def set_error_handler_process(self, process):
        self._error_process = process

    def external_callback(self, callback):
        self._callback = callback

    @handler_header
    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary:
            {
                'status': ['result', 'error'],
                'data': [optional] result data dictionary,
                'type': [optional] type of result/error data,
                'details': [optional] error data dictionary
            }
        """
        if result is not None:
            if 'status' in result:
                if result['status'] == STATUS_ERROR and self._error_process is not None:
                    self._error_process.run(self._worker, **result)
                elif result['status'] == STATUS_RESULT:
                    if result.get('type', None) == RTYPE_JOB_LIST:
                        data = result['data']
                        self._next_process.run(self._worker, kwargs_list_for_results_gatherer=data[0], **data[1])
                    else:
                        self._next_process.run(self._worker, **result['data'])
            else:
                self._next_process.run(self._worker, **result)

    @staticmethod
    def job(callback_code, **kwargs):
        pass

    @staticmethod
    def process(**kwargs):
        """
          Method for handle worker-independent process functionality.
        :param kwargs: settings dictionary
        """
        pass

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        raise NotImplementedError

    def _run(self, worker, job, kwargs_list_for_results_gatherer=None, **kwargs):
        if worker is not None:
            worker.run_job(job, callback=self.handler,
                           kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer, **kwargs)

    def _run_external(self, worker, job, kwargs_list_for_results_gatherer=None, **kwargs):
        if worker is not None:
            worker.run_job(job, callback=self._callback,
                           kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer, **kwargs)

    def _handler_logger_info(self, result):
        logger.debug("+++++++++++++++++++++++++++++++++++")
        logger.debug("%s::Handler", self._classname)
        logger.debug(result)
        logger.debug("+++++++++++++++++++++++++++++++++++")

    @staticmethod
    def _job_logger_info(class_name, **kwargs):
        logger.debug("-----------------------------------")
        logger.debug("%s::Job", class_name)
        logger.debug(kwargs)
        logger.debug("-----------------------------------")

    @staticmethod
    def _process_logger_info(class_name, **kwargs):
        logger.debug("===================================")
        logger.debug("%s::Process", class_name)
        logger.debug(kwargs)
        logger.debug("===================================")

    @staticmethod
    def create_result_message(result, result_type=None):
        res = {'status': STATUS_RESULT, 'data': result}
        if result_type is not None:
            res.update({'type': result_type})
        return res

    @staticmethod
    def create_error_message(details):
        return {'status': STATUS_ERROR, 'details': details}
