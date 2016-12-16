from ..test_dataformat import TestDataFormat


def TestDataFormat_test():
    dataformat = TestDataFormat()
    assert dataformat is not None
    test_data = "Test Data"
    assert dataformat.printData() == "TestDataFormat: Test"
    assert dataformat.parseData(test_data) == {"text": test_data}
