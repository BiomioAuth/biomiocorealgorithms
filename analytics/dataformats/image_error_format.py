from base_dataformat import BaseDataFormat


class ImageErrorFormat(BaseDataFormat):
    def __init__(self, data=None):
        BaseDataFormat.__init__(self, data)

    def printData(self):
        return """[{}] Image File: [{}]. Error::{}\n""".format(self._datetime, self._data['path'],
                                                               self._data['message'])

    def parseData(self, dataline):
        result = {}
        if dataline is None:
            return result
        strlist = dataline.split(']')
        result.update({'date': strlist[0].split('[')[-1].replace('\n', ''),
                       'path': strlist[1].split('[')[-1].replace('\n', ''),
                       'message': strlist[2].split('. ')[-1].replace('\n', '')})
        return result
