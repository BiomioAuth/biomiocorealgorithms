from ..rotation_detect_algorithm import RotationDetectionAlgorithm
import numpy
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101_revert.jpg")


def RotationDetectionAlgorithm_test():
    algo = RotationDetectionAlgorithm()
    assert algo is not None
    img = cv2.imread(TEST_IMAGE_PATH)
    res = algo.apply({'img': img})
    assert res is not None
    assert res['img'].shape == (img.shape[1], img.shape[0], img.shape[2])
    assert numpy.array_equal(res['img'][0, res['img'].shape[1] - 1], img[0, 0])
