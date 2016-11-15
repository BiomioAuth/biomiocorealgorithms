"""
OpenCV Tools
System Module Test Driver
Test Driver of the implementation of functions for image loading and saving based on OpenCV.

 Types of methods:
    load - load image using file path in some type;
    save - save image object in file in some type;
"""
from ..system import loadIplImage, loadNumpyImage, saveNumpyImage, saveKeypoints
import numpy
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")
TEST_SAVE_PATH = os.path.join(scriptDir, "test_data", "test.jpg")


def loadIplImage_test():
    img = loadIplImage(TEST_IMAGE_PATH)
    assert img is not None


def loadNumpyImage_test():
    img = loadNumpyImage(TEST_IMAGE_PATH)
    assert img is not None


def saveNumpyImage_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    assert saveNumpyImage(TEST_SAVE_PATH, img)
    assert os.path.exists(TEST_SAVE_PATH)
    saved_img = cv2.imread(TEST_SAVE_PATH)
    assert saved_img is not None
    os.remove(TEST_SAVE_PATH)


def saveKeypoints_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    keypoints = [cv2.KeyPoint(0.13, 0.42, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(4.13, 5.01, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(10.13, 20.42, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(30.13, 10.98, 14.2, 0.0, 2.3112, 0, -1)]
    assert saveKeypoints(TEST_SAVE_PATH, {'data': img, 'keypoints': keypoints})
    assert os.path.exists(TEST_SAVE_PATH)
    saved_img = cv2.imread(TEST_SAVE_PATH)
    assert saved_img is not None
    assert not numpy.array_equal(saved_img, img)
    os.remove(TEST_SAVE_PATH)
