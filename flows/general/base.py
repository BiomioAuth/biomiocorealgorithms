class IAlgorithm:
    def apply(self, data):
        raise NotImplementedError

    def clean(self):
        pass


class AlgorithmFlow(IAlgorithm):
    def __init__(self):
        self._stages = self.defaultSettings()
        self._flow = []

    def flow(self):
        return self._flow, self._stages

    def addStage(self, key, stage=None):
        self._flow.append(key)
        if stage is not None:
            self._stages[key] = stage

    def removeStage(self, key):
        self._flow.remove(key)
        del self._stages[key]

    @staticmethod
    def defaultSettings():
        return {}


class LinearAlgorithmFlow(AlgorithmFlow):
    def __init__(self):
        AlgorithmFlow.__init__(self)

    def apply(self, data):
        res = data
        for stage in self._flow:
            res = self._stages.get(stage).apply(res)
        return res
