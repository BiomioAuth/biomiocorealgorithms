from base_dataformat import BaseDataFormat


class TestDataFormat(BaseDataFormat):
    def __init__(self):
        BaseDataFormat.__init__(self, None)

    def printData(self):
        return "TestDataFormat: Test"

    def parseData(self, dataline):
        result = {"text": dataline}
        return result
