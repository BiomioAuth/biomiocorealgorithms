from ..base_dataformat import BaseDataFormat
import datetime


def BaseDataFormat_test():
    data_format = BaseDataFormat()
    assert data_format is not None
    data_format.setData("!!!")
    assert data_format._data == "!!!"
    t = datetime.datetime.now()
    data_format.updateDateTime(t)
    assert data_format._datetime == t
    data_format.updateDateTime()
    assert data_format._datetime != t
