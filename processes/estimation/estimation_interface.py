class AlgorithmEstimation:

    @staticmethod
    def exportDatabase(data):
        raise NotImplementedError

    @staticmethod
    def importDatabase(data):
        raise NotImplementedError

    def estimate_training(self, data, database):
        raise NotImplementedError

    def estimate_verification(self, data, database):
        raise NotImplementedError