from ..general.decorators import job_header, process_header, store_job_result
from ..general.process_interface import AlgorithmProcessInterface
from ...flows import OpenFaceSimpleDistanceEstimation


def job(callback_code, **kwargs):
    DistanceEstimationProcess.job(callback_code, **kwargs)


class DistanceEstimationProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)

    @classmethod
    @store_job_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        record = DistanceEstimationProcess.process(**kwargs)
        return DistanceEstimationProcess.create_result_message(record)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        if kwargs is None:
            # TODO: Write Error handler
            return {'result': False}
        distance_estimation = OpenFaceSimpleDistanceEstimation()
        database = kwargs.get('database')
        if kwargs.get('database_loader') is not None:
            database = kwargs.get('database_loader')(database)
        threshold = database.get('threshold', None)
        if threshold is None:
            threshold = kwargs.get('threshold', 0.0)
        dist = distance_estimation.apply({'data': kwargs['rep'], 'database': database,
                                          'options': kwargs.get('options', {})})
        result = kwargs.copy()
        result.update({'result': dist['result'] < threshold})
        return result

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
