"""
OpenCV Tools
Types Module Test Driver
Test Driver of the implementation of functions for basic type conversion based on OpenCV.
"""
from ..types import numpy_darrayToIplImage, iplImageToNumpy_darray, numpy_ndarrayToList, listToNumpy_ndarray, \
    classKeyPointToArray, arrayToKeyPointClass, copyKeyPoint, isEqual
import numpy
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


def numpy_darrayToIplImage_test():
    test_img = cv2.imread(TEST_IMAGE_PATH)
    img = numpy_darrayToIplImage(test_img)
    assert img is not None
    assert isinstance(img, cv2.cv.iplimage)


def iplImageToNumpy_darray_test():
    test_img = cv2.cv.LoadImage(TEST_IMAGE_PATH)
    img = iplImageToNumpy_darray(test_img)
    assert img is not None
    assert isinstance(img, numpy.ndarray)


def numpy_ndarrayToList_test():
    test_ndarray = numpy.zeros((2, 2), dtype=numpy.float32)
    test_list = numpy_ndarrayToList(test_ndarray)
    assert test_list is not None
    assert len(test_list) == 2
    assert len(test_list[0]) == 2


def listToNumpy_ndarray_test():
    test_list = [[1, 1], [1, 1]]
    test_ndarray = listToNumpy_ndarray(test_list, dtype=numpy.float32)
    assert test_ndarray is not None
    assert test_ndarray.shape == (2, 2)


def classKeyPointToArray_test():
    test_point = cv2.KeyPoint(0.13, 0.42, 14.2, 0.0, 2.3112, 0, -1)
    arr_point = classKeyPointToArray(test_point, with_points=True)
    assert arr_point is not None
    assert arr_point[0] == test_point.pt[0]
    assert arr_point[1] == test_point.pt[1]
    assert arr_point[2] == test_point.size
    assert arr_point[3] == test_point.angle
    assert arr_point[4] == test_point.response
    assert arr_point[5] == test_point.octave


def arrayToKeyPointClass_test():
    arr_point = numpy.array([13, 42, 14.0, 0.0, 2.0, 0])
    test_point = arrayToKeyPointClass(arr_point, with_points=True)
    assert test_point is not None
    assert test_point.pt[0] == arr_point[0]
    assert test_point.pt[1] == arr_point[1]
    assert test_point.size == arr_point[2]
    assert test_point.angle == arr_point[3]
    assert test_point.response == arr_point[4]
    assert test_point.octave == arr_point[5]


def copyKeyPoint_test():
    test_point = cv2.KeyPoint(0.13, 0.42, 14.2, 0.0, 2.3112, 0, -1)
    copy_point = copyKeyPoint(test_point)
    assert test_point.pt == copy_point.pt
    assert test_point.size == copy_point.size
    assert test_point.angle == copy_point.angle
    assert test_point.response == copy_point.response
    assert test_point.octave == copy_point.octave
    assert test_point.class_id == copy_point.class_id


def isEqual_test():
    test_ndarray1 = numpy.zeros((2, 2, 3), dtype=numpy.float32)
    test_ndarray2 = numpy.zeros((2, 2, 3), dtype=numpy.float32)
    assert isEqual(test_ndarray1, test_ndarray2)
