from ..hist_transform import histtruncate
from ...cvtools import grayscale
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


def histtruncate_test():
    img = grayscale(cv2.imread(TEST_IMAGE_PATH))
    res = histtruncate(img, 5, 25)
    assert res is not None
    assert res[0].shape == img.shape
    assert res[1] is not None
    assert res[2] is not None
