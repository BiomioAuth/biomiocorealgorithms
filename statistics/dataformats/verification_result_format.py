from base_dataformat import BaseDataFormat

class VerificationResultFormat(BaseDataFormat):
    def __init__(self, data=None):
        BaseDataFormat.__init__(self, data)

    def printData(self):
        return """
        [{}] Verification Result: {userID: {}, probeID: {}, threshold: {}, status: {}, result: {}}
        """.format(self._datatime, self._data['userID'], self._data['probeID'],
                   self._data['threshold'], self._data['status'], self._data['result'])
