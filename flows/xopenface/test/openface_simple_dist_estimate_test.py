from ..openface_simple_dist_estimate import OpenFaceSimpleDistanceEstimation
import numpy


def OpenFaceSimpleDistanceEstimation_test():
    estimation = OpenFaceSimpleDistanceEstimation()
    assert estimation is not None
    data_list = []
    for inx in range(0, 5, 1):
        rep = numpy.zeros(128)
        rep.fill(2)
        data_list.append({'rep': rep})
    database = {'data': data_list}
    data = {'rep': numpy.zeros(128)}
    res = estimation.apply({'database': database, 'data': data})
    assert res is not None
    assert res['result'] is not None
    assert int(res['result']**2) == int(512.0)
