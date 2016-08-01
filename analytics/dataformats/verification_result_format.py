from base_dataformat import BaseDataFormat
import json

class VerificationResultFormat(BaseDataFormat):
    def __init__(self, data=None):
        BaseDataFormat.__init__(self, data)

    def printData(self):
        params = """userID: {}, probeID: {}, data folder: {}, threshold: {}, status: {}, result: {}""".format(
            self._data['userID'], self._data['probeID'], self._data['data_path'], self._data['threshold'],
            self._data['status'], self._data['result'])
        return """[{}] Verification Result: [{}]\n""".format(self._datetime, params)

    def parseData(self, dataline):
        result = {}
        if dataline is None:
            return result
        strlist = dataline.split(']')
        result.update({'date': strlist[0].split('[')[-1].replace('\n', '')})
        paramsstr = strlist[1].split('[')[1]
        params_list = paramsstr.split(',')
        for params in params_list:
            key, value = params.split(': ')
            result.update({key.replace(' ', ''): value})
        return result
