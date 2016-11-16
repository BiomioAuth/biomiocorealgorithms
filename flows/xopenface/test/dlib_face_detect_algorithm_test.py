from ..dlib_face_detect_algorithm import DLibFaceDetectionAlgorithm
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")
DLIB_MODEL_PATH = os.path.join(scriptDir, "..", "..", "..", "data", "shape_predictor_68_face_landmarks.dat")
OPENFACE_IMGDIM = 96


def read_image(path):
    assert os.path.exists(TEST_IMAGE_PATH), "Test image doesn't found."
    return cv2.imread(path)


def DLibFaceDetectionAlgorithm_test():
    assert os.path.exists(TEST_IMAGE_PATH), "Test image doesn't found."
    assert os.path.exists(DLIB_MODEL_PATH), "Test DLib face landmarks pre-trained model doesn't found."
    imgDim = OPENFACE_IMGDIM
    algo = DLibFaceDetectionAlgorithm({'imgDim': imgDim, 'dlibFacePredictor': DLIB_MODEL_PATH})
    assert algo is not None
    res = algo.apply({'img': read_image(TEST_IMAGE_PATH)})
    assert res is not None
    assert res['img'] is not None
    assert res['img'].shape == (imgDim, imgDim, 3)
