from ...dataformats.test_dataformat import TestDataFormat
from ..dataformat_stream import DataFormatStream
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_FILE = os.path.join(scriptDir, "test.txt")


def DataFormatStream_test():
    stream = DataFormatStream(TEST_DATA_FILE)
    assert stream is not None
    stream.addFormat(TestDataFormat())
    stream.write()
    assert os.path.exists(TEST_DATA_FILE)
    os.remove(TEST_DATA_FILE)
