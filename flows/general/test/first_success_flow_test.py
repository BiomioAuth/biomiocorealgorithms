from ..first_success_flow import FirstSuccessFlow
from ..test_algorithm import TestAlgorithm


def result_counting(data):
    if data is not None:
        res = data.get('result', [])
        if len(res) > 0:
            return res[0]
    return False


def FirstSuccessFlow_test():
    flow_empty = FirstSuccessFlow()
    assert flow_empty is not None
    flow_empty.addStage('test0', TestAlgorithm(False))
    flow_empty.addStage('test1', TestAlgorithm())
    flow_empty.addStage('test2', TestAlgorithm(False))
    flow_empty.addStage('test3', TestAlgorithm())
    res = flow_empty.apply({})
    assert res is not None
    assert len(res['result']) == 1

    flow = FirstSuccessFlow(result_counting)
    assert flow is not None
    flow.addStage('test0', TestAlgorithm(False))
    flow.addStage('test1', TestAlgorithm())
    flow.addStage('test2', TestAlgorithm(False))
    flow.addStage('test3', TestAlgorithm())
    res = flow.apply({})
    assert res is not None
    assert len(res['result']) == 1
    for r in res['result']:
        assert r
