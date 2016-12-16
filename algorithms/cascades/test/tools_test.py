from ..tools import getROIImage, isRectangle, inside, skipEmptyRectangles, loadScript
from .. import SCRIPTS_PATH
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")
TEST_SCRIPT_REL_PATH = "main_rotation_haarcascade_face_eyes.json"
TEST_SCRIPT_PATH = os.path.join(SCRIPTS_PATH, TEST_SCRIPT_REL_PATH)


def getROIImage_test():
    r = [10, 20, 200, 250]
    res = getROIImage(cv2.imread(TEST_IMAGE_PATH), r)
    assert res is not None
    assert res.shape == (250, 200, 3)


def isRectangle_test():
    r = [0, 0, 10, 20]
    assert isRectangle(rect=r)


def inside_test():
    template = [0, 5, 300, 400]
    testTrue = [20, 25, 100, 100]
    testFalse = [0, 0, 200, 200]
    assert inside(testTrue, template)
    assert inside(testFalse, template, ds=0.1)
    assert inside(testFalse, template) is False


def skipEmptyRectangles_test():
    rects = [[10, 10, 20, 30], [], [20, 30, 40], [0, 0]]
    res = skipEmptyRectangles(rects)
    assert res is not None
    assert len(res) == 1


def loadScript_test():
    script1 = loadScript(TEST_SCRIPT_REL_PATH, relative=True)
    assert script1 is not None
    assert script1.keys() > 0
    script2 = loadScript(TEST_SCRIPT_PATH)
    assert script2 is not None
    assert script2.keys() > 0
