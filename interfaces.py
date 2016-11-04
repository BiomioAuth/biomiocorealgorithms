class AlgorithmInterface:

    def training(self, callback=None, **kwargs):
        raise NotImplementedError

    def apply(self, callback=None, **kwargs):
        raise NotImplementedError
