from algorithms.interfaces import AlgorithmProcessInterface, logger
from biomio.algorithms.recognition.processes.defs import STATUS_ERROR, STATUS_RESULT, ERROR_FORMAT, INTERNAL_TRAINING_ERROR
from biomio.algorithms.recognition.processes.messages import create_error_message, create_result_message
from biomio.algorithms.recognition.processes.defs import INVALID_ALGORITHM_SETTINGS, UNKNOWN_ERROR
from algorithms.imgobj import loadImageObject
from biomio.algorithms.recognition.processes.settings.settings import get_settings
from biomio.algorithms.recognition.processes.handling import save_temp_data

class TrainingProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path):
        AlgorithmProcessInterface.__init__(self)
        self._classname = "TrainingProcess"
        self._temp_data_path = temp_data_path
        self._detect_process = AlgorithmProcessInterface()
        self._rotate_process = AlgorithmProcessInterface()

    def set_data_detection_process(self, process):
        self._detect_process = process

    def set_data_rotation_process(self, process):
        self._rotate_process = process

    def handler(self, result):
        self._handler_logger_info(result)
        if result is not None:
            if result['status'] == STATUS_ERROR:
                pass
            elif result['status'] == STATUS_RESULT:
                worker = WorkerInterface.instance()
                res = result.get('data', [])
                if result['type'] == 'detection' and len(res) == 1:
                    self._detect_process.run(worker, **res[0])
                elif result['type'] == 'rotation' and len(res) == 2:
                    self._rotate_process.run(worker, kwargs_list_for_results_gatherer=res[0], **res[1])
                else:
                    logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, "Invalid Data Format."))
                    worker.run_job(self._error_process.job, callback=self._error_process.handler,
                                   kwargs_list_for_results_gatherer=res[0], **res[1])
            else:
                logger.info(ERROR_FORMAT % (UNKNOWN_ERROR, "Unknown Message"))
        else:
            logger.algo_logger.info(ERROR_FORMAT % (UNKNOWN_ERROR, "Message is empty."))

    def job(self, callback_code, **kwargs):
        self._job_logger_info(**kwargs)
        record = self.process(**kwargs)
        logger.algo_logger.debug("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        logger.algo_logger.debug(record)
        logger.algo_logger.debug("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=record, callback_code=callback_code)

    def process(self, **kwargs):
        self._process_logger_info(**kwargs)
        imgobj = loadImageObject(kwargs['path'])
        imgobj.update(**kwargs)
        if not imgobj:
            record = create_error_message(INVALID_ALGORITHM_SETTINGS, 'path',
                                          "Such data %s doesn't exists." % kwargs['path'])
            logger.info(ERROR_FORMAT % (record['type'], record['details']['message']))
        else:
            settings = get_settings(imgobj['algoID'])
            if settings['use_roi'] and settings['rotation_script']:
                logger.debug("TEST ROTATION")
                job_list = []
                for i in range(0, 4, 1):
                    job_list.append({'angle': i})
                training_process_data = save_temp_data(imgobj, self._temp_data_path, ['data'])
                record = create_result_message([job_list, {'data_file': training_process_data}], 'rotation')
            else:
                logger.debug("TEST WITHOUT ROTATION")
                imgobj['roi'] = imgobj['data']
                detection_process_data = save_temp_data(imgobj, self._temp_data_path, ['data', 'roi'])
                record = create_result_message([{'data_file': detection_process_data}], 'detection')
        return record
