from base_dataformat import BaseDataFormat

class ImageErrorFormat(BaseDataFormat):
    def __init__(self, data=None):
        BaseDataFormat.__init__(self, data)

    def printData(self):
        return """[{}] Image File: [{}]. Error::{}""".format(self._datatime, self._data['path'], self._data['message'])
