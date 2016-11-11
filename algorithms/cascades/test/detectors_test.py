from ..detectors import ROIDetectorInterface, OptimalROIDetector, OptimalROIDetectorSAoS
from ....imgobj import loadImageObject
import numpy
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_01_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")
TEST_IMAGE_02_PATH = os.path.join(scriptDir, "test_data", "DI0102.jpg")
TEST_IMAGE_03_PATH = os.path.join(scriptDir, "test_data", "DI0201.jpg")


def ROIDetectorInterface_test():
    interface = ROIDetectorInterface()
    assert interface is not None


def OptimalROIDetector_test():
    detector = OptimalROIDetector()
    assert detector is not None
    paths = [TEST_IMAGE_01_PATH, TEST_IMAGE_02_PATH, TEST_IMAGE_03_PATH]
    data = []
    for path in paths:
        data.append(loadImageObject(path))
    res = detector.detect(data)
    assert res is not None
    for r in res:
        assert r is not None
        assert r['data'] is not None
        assert isinstance(r['data'], numpy.ndarray)
        assert r['data'].dtype == numpy.uint8


def OptimalROIDetectorSAoS_test():
    detector = OptimalROIDetectorSAoS()
    assert detector is not None
    paths = [TEST_IMAGE_01_PATH, TEST_IMAGE_02_PATH, TEST_IMAGE_03_PATH]
    data = []
    for path in paths:
        data.append(loadImageObject(path))
    res = detector.detect(data)
    assert res is not None
    for r in res:
        assert r is not None
        assert r['data'] is not None
        assert isinstance(r['data'], numpy.ndarray)
        assert r['data'].dtype == numpy.uint8
