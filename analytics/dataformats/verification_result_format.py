from base_dataformat import BaseDataFormat

class VerificationResultFormat(BaseDataFormat):
    def __init__(self, data=None):
        BaseDataFormat.__init__(self, data)

    def printData(self):
        params = """userID: {}, probeID: {}, data folder: {}, threshold: {}, status: {}, result: {}""".format(
            self._data['userID'], self._data['probeID'], self._data['data_path'], self._data['threshold'],
            self._data['status'], self._data['result'])
        return """[{}] Verification Result: [{}]\n""".format(self._datetime, params)
