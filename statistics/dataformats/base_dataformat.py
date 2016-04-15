import datetime

class BaseDataFormat:
    def __init__(self, data=None):
        self._data = data
        self._datatime = None

    def setData(self, data):
        if self._data != data:
            self._data = data

    def updateDataTime(self, datatime=None):
        if datatime is None:
            datatime = datetime.datetime.now()
        if self._datatime != datatime:
            self._datatime = datatime

    def printData(self):
        raise NotImplementedError
