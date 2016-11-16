from base import IAlgorithm


class TestAlgorithm(IAlgorithm):
    def __init__(self, default=True):
        self._default = default

    def apply(self, data):
        test_data = [] if data is None else data.get('result', [])
        test_data.append(self._default)
        return {'result': test_data}
