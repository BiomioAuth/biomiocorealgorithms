from ..scripts_detectors import DetectorStage, CascadesDetectionInterface, RotatedCascadesDetector
from .. tools import loadScript
import numpy
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")
TEST_IMAGE_REV_PATH = os.path.join(scriptDir, "test_data", "DI0101_revert.jpg")


def DetectorStage_test():
    stage = DetectorStage()
    assert stage is not None
    assert stage.name == "default"
    assert stage.type == "main"
    assert isinstance(stage.stages, list) and len(stage.stages) == 0
    assert isinstance(stage.classifiers, list) and len(stage.classifiers) == 0
    assert stage.strategy is None


def CascadesDetectionInterface_test():
    detector = CascadesDetectionInterface(loadScript("main_haarcascade_face_size.json", True))
    assert detector is not None
    res = detector.detect(cv2.imread(TEST_IMAGE_PATH))
    assert res is not None
    assert isinstance(res[0], numpy.ndarray)
    assert res[0].dtype == numpy.uint8
    assert res[1] is not None
    assert len(res[1][0]) == 4


def RotatedCascadesDetector_test():
    detector = RotatedCascadesDetector(loadScript("main_rotation_haarcascade_face_eyes.json", True), loadScript(""))
    assert detector is not None
    img = cv2.imread(TEST_IMAGE_PATH)
    res = detector.detect(img)
    assert res is not None
    assert res[0].shape == img.shape
    assert res[1] == []
    img2 = cv2.imread(TEST_IMAGE_REV_PATH)
    res = detector.detect(img2)
    assert res is not None
    assert res[0].shape == (img2.shape[1], img2.shape[0], img2.shape[2])
    assert res[1] == []
