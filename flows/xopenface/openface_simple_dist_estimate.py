from ..general.decorators import algorithm_header
import scipy.spatial.distance as distance
from ..general.base import IAlgorithm
import sys


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

    @algorithm_header
    def apply(self, data):
        database = data.get('database')
        tdata = data.get('data')
        result = data.copy()
        if database is None or tdata is None or len(database.get('data', [])) <= 0:
            # TODO: Write Error handler
            result.update({'result': sys.float_info.max})
            return result
        avg = 0
        for item in database.get('data', []):
            if len(item['rep']) <= 0:
                continue
            avg += distance.euclidean(tdata['rep'], item['rep'])
        avg /= len(database.get('data', []))
        result.update({'result': avg})
        return result
