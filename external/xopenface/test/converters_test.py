from ..converters import toNumpyArray, toCVShape, toCV2Image, toTorchShape, toTorchImage
import lutorpy as lua
import numpy as np
import cv2
import os

lua.require('torch')
lua.require('image')


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.png")


def toNumpyArray_test():
    ttensor = torch.Tensor(2, 4)._fill(2)
    t_array = toNumpyArray(ttensor)
    assert t_array is not None
    assert t_array.shape == (2, 4)
    assert t_array[0, 0] == 2


def toCVShape_test():
    timage = image.load(TEST_IMAGE_PATH, 3, 'float')
    rimage = toCVShape(timage, fromTensor=True)
    assert rimage is not None
    assert timage._size(1) == rimage.shape[2]
    assert timage._size(2) == rimage.shape[0]
    assert timage._size(3) == rimage.shape[1]
    assert timage[0][2][2] == rimage[2, 2, 0]


def toCV2Image_test():
    timage = image.load(TEST_IMAGE_PATH, 3, 'float')
    rimage = toCV2Image(timage, fromTensor=True)
    assert rimage is not None
    assert timage._size(1) == rimage.shape[2]
    assert timage._size(2) == rimage.shape[0]
    assert timage._size(3) == rimage.shape[1]
    assert isinstance(rimage[0, 0, 0], np.uint8)
    assert int(timage[0][2][2] * 255) == rimage[2, 2, 2]


def toTorchShape_test():
    timage = cv2.imread(TEST_IMAGE_PATH)
    rimage = toTorchShape(timage)
    assert rimage is not None
    assert timage.shape[0] == rimage.shape[1]
    assert timage.shape[1] == rimage.shape[2]
    assert timage.shape[2] == rimage.shape[0]
    assert timage[2, 2, 0] == rimage[0][2][2]


def toTorchImage_test():
    timage = cv2.imread(TEST_IMAGE_PATH)
    rimage = toTorchImage(timage)
    assert rimage is not None
    assert timage.shape[0] == rimage.shape[1]
    assert timage.shape[1] == rimage.shape[2]
    assert timage.shape[2] == rimage.shape[0]
    assert isinstance(rimage[0, 0, 0], np.float64)
    assert timage[2, 2, 0] / 255.0 == rimage[0][2][2]
