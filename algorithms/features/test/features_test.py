from ..features import grayscale, grayscale_and_equalize, self_quotient_image, gabor_image, BaseDecorator, \
    FeatureDetector, FEATURES_GRAYSCALE, FEATURES_EQUALIZE, FEATURES_GABORIMAGE, FEATURES_SQIMAGE
from ..detectors import BRISKDetector
import numpy
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


class TestDetector:
    def __init__(self, mode):
        self._mode = mode

    @grayscale
    def test_grayscale(self, image):
        return image

    @grayscale_and_equalize
    def test_grayscale_and_equalize(self, image):
        return image

    @self_quotient_image
    def test_self_quotient_image(self, image):
        return image

    @gabor_image
    def test_gabor_image(self, image):
        return image


def grayscale_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    detector = TestDetector(FEATURES_GRAYSCALE)
    assert detector is not None
    assert not numpy.array_equal(detector.test_grayscale(img), img)


def grayscale_and_equalize_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    detector = TestDetector(FEATURES_EQUALIZE)
    assert detector is not None
    assert not numpy.array_equal(detector.test_grayscale_and_equalize(img), img)


def self_quotient_image_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    detector = TestDetector(FEATURES_SQIMAGE)
    assert detector is not None
    assert not numpy.array_equal(detector.test_self_quotient_image(img), img)


def gabor_image_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    detector = TestDetector(FEATURES_GABORIMAGE)
    assert detector is not None
    assert not numpy.array_equal(detector.test_gabor_image(img), img)


def BaseDecorator_test():
    decorator = BaseDecorator(None)
    assert decorator is not None


def FeatureDetector_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    detector = FeatureDetector(BRISKDetector())
    assert detector is not None
    res = detector.detect(img)
    assert res is not None
    assert numpy.array_equal(res['data'], img)
    assert res['keypoints'] is not None
    assert len(res['keypoints']) > 0
    assert isinstance(res['keypoints'][0], type(cv2.KeyPoint()))
    res2 = detector.compute(img, res['keypoints'])
    assert res2 is not None
    assert numpy.array_equal(res2['data'], img)
    assert res2['keypoints'] is not None
    assert len(res2['keypoints']) > 0
    assert isinstance(res2['keypoints'][0], type(cv2.KeyPoint()))
    assert res2['descriptors'] is not None
    assert len(res2['descriptors']) > 0
    assert isinstance(res2['descriptors'][0], numpy.ndarray)
    res3 = detector.detectAndCompute(img)
    assert res3 is not None
    assert numpy.array_equal(res3['data'], img)
    assert res3['keypoints'] is not None
    assert len(res3['keypoints']) > 0
    assert isinstance(res3['keypoints'][0], type(cv2.KeyPoint()))
    assert res3['descriptors'] is not None
    assert len(res3['descriptors']) > 0
    assert isinstance(res3['descriptors'][0], numpy.ndarray)
    detector2 = FeatureDetector(BRISKDetector(), mode=None)
    assert numpy.array_equal(detector2.transform_image(img), img)
