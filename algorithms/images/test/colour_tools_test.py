from ..colour_tools import rgb_to_hsv, hsv_to_rgb, hsv_values_extraction
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


def rgb_to_hsv_test():
    white = [255, 255, 255]
    black = [0, 0, 0]
    res = rgb_to_hsv(white)
    assert res is not None
    assert res == [0, 0.0, 1.0]
    res = rgb_to_hsv(black)
    assert res is not None
    assert res == [0, 0.0, 0.0]


def hsv_to_rgb_test():
    white = [0, 0.0, 1.0]
    res = hsv_to_rgb(white)
    assert res is not None
    assert res == [255, 255, 255]
    black = [0, 0.0, 0.0]
    res = hsv_to_rgb(black)
    assert res is not None
    assert res == [0, 0, 0]


def hsv_values_extraction_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    res = hsv_values_extraction(img)
    assert res is not None
    assert res.shape == img.shape
