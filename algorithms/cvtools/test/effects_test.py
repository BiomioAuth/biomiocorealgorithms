"""
OpenCV Tools
Effects Module Test Driver
Test Driver of the implementation of functions for image processing based on OpenCV.
"""
from ..effects import grayscale, equalizeHist, grayscaleAndEqualize, \
    binarization, gaussianBlurring, rotate90
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


def read_image(path):
    assert os.path.exists(TEST_IMAGE_PATH), "Test image doesn't found."
    return cv2.imread(path)


def grayscale_test():
    gray = grayscale(read_image(TEST_IMAGE_PATH))
    assert gray is not None


def equalizeHist_test():
    eqHist = equalizeHist(grayscale(read_image(TEST_IMAGE_PATH)))
    assert eqHist is not None


def grayscaleAndEqualize_test():
    grayEq = grayscaleAndEqualize(read_image(TEST_IMAGE_PATH))
    assert grayEq is not None


def binarization_test():
    binImg = binarization(read_image(TEST_IMAGE_PATH))
    assert binImg is not None
    pixel = binImg[0, 0]
    assert pixel[0] == 1 or pixel[0] == 0
    assert pixel[1] == 1 or pixel[1] == 0
    assert pixel[2] == 1 or pixel[2] == 0


def gaussianBlurring_test():
    gBlur = gaussianBlurring(read_image(TEST_IMAGE_PATH), (7, 7))
    assert gBlur is not None


def rotate90_test():
    rImg = rotate90(read_image(TEST_IMAGE_PATH))
    assert rImg is not None
