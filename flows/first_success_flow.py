from base import AlgorithmFlow


class FirstSuccessFlow(AlgorithmFlow):
    def __init__(self, functor=None):
        AlgorithmFlow.__init__(self)
        self._functor = functor

    def apply(self, data):
        res = data
        for stage in self._flow:
            res = data.copy()
            res = self._stages.get(stage).apply(res)
            if self._functor is not None:
                if self._functor(res):
                    return res
            else:
                if res is not None:
                    return res
        return res
