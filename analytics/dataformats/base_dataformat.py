import datetime


class BaseDataFormat:
    def __init__(self, data=None):
        self._data = data
        self._datetime = None

    def setData(self, data):
        if self._data != data:
            self._data = data

    def updateDateTime(self, dtime=None):
        if dtime is None:
            dtime = datetime.datetime.now()
        if self._datetime != dtime:
            self._datetime = dtime

    def printData(self):
        raise NotImplementedError

    def parseData(self, dataline):
        raise NotImplementedError
