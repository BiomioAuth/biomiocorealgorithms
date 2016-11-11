from ..classifiers import CascadeClassifierSettings, CascadeROIDetector
from .. import CASCADES_PATH
import numpy
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


def CascadeClassifierSettings_test():
    default_settings = {'Scale Factor': 1.1, 'Minimum Neighbors': 3,
                        'Minimum Size': (30, 30), 'Maximum Size': (1000, 1000)}
    test_settings = {'Scale Factor': 1.5, 'Minimum Neighbors': 1,
                     'Minimum Size': (56, 56), 'Maximum Size': (156, 156)}
    settings_obj = CascadeClassifierSettings()
    assert settings_obj is not None
    assert settings_obj.exportSettings() == default_settings
    settings_obj.importSettings(test_settings)
    assert settings_obj.exportSettings() == test_settings
    settings_obj.dump()


def CascadeROIDetector_test():
    detector = CascadeROIDetector()
    assert detector is not None
    assert detector.cascades() == []
    settings = CascadeClassifierSettings()
    settings.minNeighbors = 1
    settings.minSize = (100, 100)
    detector.classifierSettings = settings
    assert detector.classifierSettings == settings
    detector.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt.xml"))
    detector.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt_tree.xml"))
    detector.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt2.xml"))
    detector.add_cascade(os.path.join(CASCADES_PATH, "haarcascade_frontalface_default.xml"))
    assert len(detector.cascades()) == 4
    default_settings = {'Settings': settings.exportSettings(),
                        'ROI Cascades': [os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt.xml"),
                                         os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt_tree.xml"),
                                         os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt2.xml"),
                                         os.path.join(CASCADES_PATH, "haarcascade_frontalface_default.xml")]}
    test_settings = {'Settings': settings.exportSettings(),
                     'ROI Cascades': [os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt.xml"),
                                      os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt_tree.xml"),
                                      os.path.join(CASCADES_PATH, "haarcascade_frontalface_alt2.xml")]}
    assert detector.exportSettings() == default_settings
    detector = CascadeROIDetector()
    detector.importSettings(test_settings)
    assert detector.exportSettings() == test_settings
    img = cv2.imread(TEST_IMAGE_PATH)
    res = detector.detect(img, as_list=True)
    assert res is not None
    assert len(res) == len(detector.cascades())
    res = detector.detectAndJoin(img)
    assert res is not None
    assert len(res) == 4
    res = detector.detectAndJoinWithRotation(img)
    assert res is not None
    assert res[0] is not None
    assert isinstance(res[0], numpy.ndarray)
    assert res[0].dtype == numpy.uint8
    assert res[1] is not None
    assert len(res[1]) == 4
