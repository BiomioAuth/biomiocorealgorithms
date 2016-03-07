"""
OpenCV Tools
Types Module
Implementation of functions for basic type conversion based on OpenCV.
"""
import cv2.cv as cv
import numpy


def numpy_darrayToIplImage(source):
    """
    OpenCV Tools/Types Module
        Convert numpy.ndarray object to IplImage object.

    :param source: numpy.ndarray object
    :return: IplImage object
    """
    bitmap = cv.CreateImageHeader((source.shape[1], source.shape[0]), cv.IPL_DEPTH_8U, 3)
    cv.SetData(bitmap, source.tostring(), source.dtype.itemsize * 3 * source.shape[1])
    return bitmap


def iplImageToNumpy_darray(source):
    """
    OpenCV Tools/Types Module
        Convert IplImage object to numpy.ndarray object.

    :param source: IplImage object
    :return: numpy.ndarray object
    """
    return numpy.asarray(source[:, :])


def numpy_ndarrayToList(source):
    """
    OpenCV Tools/Types Module
        Convert numpy.ndarray object to list object.

    :param source: numpy.ndarray object
    :return: list object
    """
    return source.tolist()


def listToNumpy_ndarray(source, dtype=None):
    """
    OpenCV Tools/Types Module
        Convert list object to numpy.ndarray object.

    :param source: list object
    :return: numpy.ndarray object
    """
    return numpy.array(source, dtype=dtype)


def classKeyPointToArray(keypoint, with_points=False):
    """
    OpenCV Tools/Types Module
        Convert KeyPoint Class to numpy.ndarray object.
    If with_points is True, method include coordinates of keypoint 
    into output array, otherwise returns array without them.

    :param keypoint: KeyPoint OpenCV object
    :param with_points: bool flag
    :return: numpy.ndarray object
    """
    darray = []
    if with_points:
        darray.append(keypoint.pt[0])
        darray.append(keypoint.pt[1])
    darray.append(keypoint.size)
    darray.append(keypoint.angle)
    darray.append(keypoint.response)
    darray.append(keypoint.octave)
    return numpy.array(darray)


def isEqual(array1, array2):
    """
    OpenCV Tools/Types Module
        Check equality of two arrays. Returns True if arrays
    are equal, otherwise returns False.

    :param array1: numpy.ndarray object
    :param array2: numpy.ndarray object
    :return: bool
    """
    return numpy.array_equal(array1, array2)
