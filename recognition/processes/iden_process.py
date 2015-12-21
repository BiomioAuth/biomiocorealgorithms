from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY

IDENTIFICATION_PROCESS_CLASS_NAME = "RotationDetectionProcess"

def job(callback_code, **kwargs):
    IdentificationProcess.job(callback_code, **kwargs)


class IdentificationProcess(AlgorithmProcessInterface):
    def __init__(self):
        AlgorithmProcessInterface.__init__(self)
        self._classname = IDENTIFICATION_PROCESS_CLASS_NAME

    def handler(self, result):
        self._handler_logger_info(result)


    @staticmethod
    def job(callback_code, **kwargs):
        IdentificationProcess._job_logger_info(IDENTIFICATION_PROCESS_CLASS_NAME, **kwargs)
        record = IdentificationProcess.process(**kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        IdentificationProcess._process_logger_info(IDENTIFICATION_PROCESS_CLASS_NAME, **kwargs)
        """

        :param kwargs:
        :return: dict
            "cluster_size": length of cluster of the test image,
            "cluster_id": cluster ID,
            "candidates_size": number of found candidates,
            "candidates_score": dict
                <key>: <value>, where <key> - ID of database,
                                      <value> - number of candidates for this database
        """
        cluster = kwargs['cluster']
        database = kwargs['database']
        db = {
            "cluster_size": len(cluster),
            "cluster_id": kwargs["cluster_id"],
            "candidates_size": 0,
            "candidates_score": {}
        }
        for desc in cluster:
            local = database.neighbours(desc)
            db["candidates_size"] += len(local)
            for item in local:
                lcount = db["candidates_score"].get(item[1], 0)
                lcount += 1
                db["candidates_score"][item[1]] = lcount
        return db

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)