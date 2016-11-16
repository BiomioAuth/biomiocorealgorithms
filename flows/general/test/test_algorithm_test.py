from ..test_algorithm import TestAlgorithm


def TestAlgorithm_test():
    test = TestAlgorithm(False)
    assert test is not None
    res = test.apply({})
    assert res is not None
    assert len(res['result']) == 1
    for r in res['result']:
        assert not r
