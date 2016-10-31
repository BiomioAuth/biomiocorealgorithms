from ....interfaces import AlgorithmProcessInterface
import os


class MainTrainingProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)
        self._classname = "MainTrainingProcess"
        self._training_process = AlgorithmProcessInterface()

    def set_data_training_process(self, process):
        self._training_process = process

    def handler(self, result):
        raise NotImplementedError

    def job(self, callback_code, **kwargs):
        raise NotImplementedError

    def process(self, **kwargs):
        """
        Process function for training starting.

        :param kwargs: settings dictionary:
            {
                'algoID': algorithm identifier string,
                'general_data':
                {
                    'ai_code': AI code string,
                    'data_path': image data path,
                    'try_type': try type string,
                    'probe_id': probe identifier string
                },
                'providerID': provider identifier string, //identification plugin
                'userID': user identifier string,
                'data': image paths list
            }
        """
        MainTrainingProcess._process_logger_info(self._classname, **kwargs)
        if not os.path.exists(self._temp_data_path):
            os.mkdir(self._temp_data_path, 0o777)
            os.chmod(self._temp_data_path, 0o777)
        kwargs.update({'temp_data_path': self._temp_data_path})
        for image_path in kwargs["data"]:
            settings = kwargs.copy()
            del settings['data']
            settings['path'] = image_path
            self._training_process.run(self._worker, **settings)
