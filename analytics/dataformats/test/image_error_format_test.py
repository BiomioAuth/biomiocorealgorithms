from ..image_error_format import ImageErrorFormat
import datetime


def ImageErrorFormat_test():
    data_format = ImageErrorFormat()
    assert data_format is not None
    test_path = "/root/test/"
    test_message = "Print Test"
    t = datetime.datetime.now()
    test_line = """[{}] Image File: [{}]. Error::{}\n""".format(t, test_path, test_message)
    data_format.updateDateTime(t)
    data_format.setData({'path': test_path, 'message': test_message})
    printed_test = data_format.printData()
    assert printed_test == test_line
    res = data_format.parseData(printed_test)
    assert res == {'date': str(t), 'path': test_path, 'message': "Error::{}".format(test_message)}
