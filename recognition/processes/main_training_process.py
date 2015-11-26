from algorithms.interfaces import AlgorithmProcessInterface
import os

class MainTrainingProcess(AlgorithmProcessInterface):
    def __init__(self):
        AlgorithmProcessInterface.__init__(self)
        self._classname = "MainTrainingProcess"
        self._training_process = AlgorithmProcessInterface()

    def set_data_training_process(self, process):
        self._training_process = process

    def handler(self, result):
        raise NotImplementedError

    def job(self, callback_code, **kwargs):
        raise NotImplementedError

    def process(self, **kwargs):
        self._process_logger_info(kwargs)
        worker = WorkerInterface.instance()
        if not os.path.exists(TEMP_DATA_PATH):
            os.mkdir(TEMP_DATA_PATH, 0o777)
            os.chmod(TEMP_DATA_PATH, 0o777)
        for image_path in kwargs["data"]:
            settings = kwargs.copy()
            settings['path'] = image_path
            worker.run_job(self._training_process.job, callback=self._training_process.handler, **settings)
