from biomio.algorithms.flows.ialgorithm import IAlgorithm
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
        database = data.get('database')
        tdata = data.get('data')
        if database is None or tdata is None:
            # TODO: Write Error handler
            return 0
        avg = 0
        for item in database.get('data', []):
            avg += distance.euclidean(tdata['rep'], item['rep'])
        avg /= len(database.get('data', []))
        return {'result': avg}
