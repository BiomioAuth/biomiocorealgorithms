from ..verification_result_format import VerificationResultFormat
import datetime


def VerificationResultFormat_test():
    data_format = VerificationResultFormat()
    assert data_format is not None
    test_userID = "11111111111111111111"
    test_probeID = "22222222222222222222222222222"
    test_path = "/root/test/"
    test_thres = 0.5
    test_status = "Status::Test"
    test_result = True
    t = datetime.datetime.now()
    params = """userID: {}, probeID: {}, data folder: {}, threshold: {}, status: {}, result: {}""".format(
        test_userID, test_probeID, test_path, test_thres, test_status, test_result)
    test_line = """[{}] Verification Result: [{}]\n""".format(t, params)
    data_format.updateDateTime(t)
    data_format.setData({'userID': test_userID, 'probeID': test_probeID, 'data_path': test_path,
                         'threshold': test_thres, 'status': test_status, 'result': test_result})
    printed_test = data_format.printData()
    assert printed_test == test_line
    res = data_format.parseData(printed_test)
    assert res == {'status': test_status, 'threshold': str(test_thres), 'result': str(test_result),
                   'date': str(t), 'probeID': test_probeID, 'userID': test_userID, 'datafolder': test_path}
