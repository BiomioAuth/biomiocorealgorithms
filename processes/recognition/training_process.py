from ..general.defs import (STATUS_ERROR, STATUS_RESULT, ERROR_FORMAT, UNKNOWN_ERROR, INTERNAL_TRAINING_ERROR,
                            INVALID_ALGORITHM_SETTINGS)
from ..general.decorators import job_header, process_header, store_job_result, handler_header
from ..general.process_interface import AlgorithmProcessInterface, logger
from ..general.handling import save_temp_data
from ..messages import create_result_message
from settings.settings import get_settings
from ...imgobj import loadImageObject


def job(callback_code, **kwargs):
    TrainingProcess.job(callback_code, **kwargs)


class TrainingProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)
        self._detect_process = AlgorithmProcessInterface()
        self._rotate_process = AlgorithmProcessInterface()

    def set_data_detection_process(self, process):
        self._detect_process = process

    def set_data_rotation_process(self, process):
        self._rotate_process = process

    @handler_header
    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary:
        Rotation Result Type ('type'):
            {
                'status': 'result',
                'data':
                [
                    [
                        {'angle': 0},
                        {'angle': 1},
                        {'angle': 2},
                        {'angle': 3}
                    ],
                    {
                        'data_file': temp data file path
                    }
                ],
                'type': result type
            }
        """
        if result is not None:
            if result['status'] == STATUS_ERROR:
                pass
            elif result['status'] == STATUS_RESULT:
                res = result.get('data', [])
                if result['type'] == 'detection' and len(res) == 1:
                    self._detect_process.run(self._worker, **res[0])
                elif result['type'] == 'rotation' and len(res) == 2:
                    self._rotate_process.run(self._worker, kwargs_list_for_results_gatherer=res[0], **res[1])
                else:
                    logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, "Invalid Data Format."))
                    if self._error_process:
                        self._error_process.run(self._worker, **res[1])
            else:
                logger.info(ERROR_FORMAT % (UNKNOWN_ERROR, "Unknown Message"))
        else:
            logger.info(ERROR_FORMAT % (UNKNOWN_ERROR, "Message is empty."))

    @classmethod
    @store_job_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for training starting.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'path': image file path,
                'userID': user identifier string,
                'general_data':
                {
                    'ai_code': AI code string,
                    'data_path': images data path,
                    'probe_id': probe identifier string,
                    'try_type': try type string
                },
                'providerID': provider identifier string,
                'algoID': algorithm identifier string,
                'temp_data_path': temporary data path
            }
        """
        return TrainingProcess.process(**kwargs)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        temp_data_path = kwargs['temp_data_path']
        imgobj = loadImageObject(kwargs['path'])
        imgobj.update(**kwargs)
        if not imgobj:
            record = TrainingProcess.create_error_message({'type': INVALID_ALGORITHM_SETTINGS, 'param': 'path',
                                                           'message': "Such data %s doesn't exists." % kwargs['path']},
                                                          kwargs.get('options', {}))
            logger.info(ERROR_FORMAT % (record['type'], record['details']['message']))
        else:
            settings = get_settings(imgobj['algoID'])
            if settings['use_roi'] and settings['rotation_script']:
                logger.debug("TEST ROTATION")
                job_list = [{'angle': i} for i in range(0, 4, 1)]
                training_process_data = save_temp_data(imgobj, temp_data_path, ['data'])
                record = create_result_message([job_list, {'data_file': training_process_data}], 'rotation')
            else:
                logger.debug("TEST WITHOUT ROTATION")
                imgobj['roi'] = imgobj['data']
                detection_process_data = save_temp_data(imgobj, temp_data_path, ['data', 'roi'])
                record = create_result_message([{'data_file': detection_process_data}], 'detection')
        return record

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
