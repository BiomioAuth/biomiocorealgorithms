from ..cascades_face_detect_algorithm import CascadesFaceDetectionAlgorithm
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")
IMGDIM = 96


def CascadesFaceDetectionAlgorithm_test():
    algo = CascadesFaceDetectionAlgorithm({'imgDim': IMGDIM})
    assert algo is not None
    res = algo.apply({'img': cv2.imread(TEST_IMAGE_PATH), 'path': TEST_IMAGE_PATH})
    assert res is not None
    assert res['img'].shape == (IMGDIM, IMGDIM, 3)

    algo = CascadesFaceDetectionAlgorithm({'imgDim': None})
    assert algo is not None
    res = algo.apply({'img': cv2.imread(TEST_IMAGE_PATH), 'path': TEST_IMAGE_PATH})
    assert res is not None
    assert res['img'].shape[0] > 0 and res['img'].shape[1] > 0 and res['img'].shape[2] > 0
