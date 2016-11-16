from ..openface_data_rep import OpenFaceDataRepresentation
from ..dlib_face_detect_algorithm import DLibFaceDetectionAlgorithm
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")
DLIB_MODEL_PATH = os.path.join(scriptDir, "..", "..", "..", "data", "shape_predictor_68_face_landmarks.dat")
OPENFACE_MODEL_PATH = os.path.join(scriptDir, "..", "..", "..", "data", "nn4.small2.v1.t7")
OPENFACE_IMGDIM = 96


def OpenFaceDataRepresentation_test():
    algo = OpenFaceDataRepresentation({'networkModel': OPENFACE_MODEL_PATH, 'imgDim': OPENFACE_IMGDIM})
    assert algo is not None
    algo.setFaceAlignmentStage(DLibFaceDetectionAlgorithm({'dlibFacePredictor': DLIB_MODEL_PATH,
                                                           'imgDim': OPENFACE_IMGDIM}))
    res = algo.apply({'path': TEST_IMAGE_PATH})
    assert res is not None
    assert res['rep'] is not None
    assert res['rep'].shape == (128,)
