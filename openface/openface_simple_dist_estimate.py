from biomio.algorithms.flows.base import IAlgorithm
from biomio.algorithms.logger import logger
import scipy.spatial.distance as distance


class OpenFaceSimpleDistanceEstimation(IAlgorithm):
    """
    Input:
    {
        'database': database based on the training data
        {
            'data': list of training data
            {
                'rep': representation array
            }
        }
        'data': test data
        {
            'rep': representation array
        }
    }
    Output:
    {
        'result: distance between database and test data
    }
    """
    def __init__(self):
        pass

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("OpenFaceSimpleDistanceEstimation::apply")
        logger.debug(data)
        logger.debug("===================================")
        database = data.get('database')
        tdata = data.get('data')
        if database is None or tdata is None or len(database.get('data', [])) <= 0:
            # TODO: Write Error handler
            return {'result': 0}
        avg = 0
        for item in database.get('data', []):
            if len(item['rep']) <= 0:
                continue
            avg += distance.euclidean(tdata['rep'], item['rep'])
        avg /= len(database.get('data', []))
        return {'result': avg}
