from ..base import IAlgorithm, AlgorithmFlow, LinearAlgorithmFlow
from ..test_algorithm import TestAlgorithm


def ialgorithm_test():
    ialgo = IAlgorithm()
    assert ialgo is not None
    ialgo.clean()


def AlgorithmFlow_test():
    flow = AlgorithmFlow()
    assert flow is not None
    assert flow.defaultSettings() == {}
    assert flow.flow() == ([], flow.defaultSettings())
    flow.addStage('test', TestAlgorithm())
    keys, stages = flow.flow()
    assert len(keys) == 1 and keys[0] == 'test'
    assert len(stages) == 1 and isinstance(stages['test'], TestAlgorithm)
    flow.removeStage('test')
    keys, stages = flow.flow()
    assert len(keys) == 0 and len(stages) == 0


def LinearAlgorithmFlow_test():
    flow = LinearAlgorithmFlow()
    assert flow is not None
    flow.addStage('test0', TestAlgorithm())
    flow.addStage('test1', TestAlgorithm())
    flow.addStage('test2', TestAlgorithm())
    keys, stages = flow.flow()
    assert len(keys) == 3 and len(stages) == 3
    for inx in range(0, 3, 1):
        assert keys[inx] == 'test' + str(inx)
        assert isinstance(stages['test' + str(inx)], TestAlgorithm)
    res = flow.apply({})
    assert len(res['result']) == 3
    for r in res['result']:
        assert r
