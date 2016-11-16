from ..detectors import BaseDetector, BRISKDetectorSettings, BRISKDetector, ORBDetectorSettings, \
    ORBDetector, SURFDetectorSettings, SURFDetector, mahotasSURFDetectorSettings, mahotasSURFDetector
import numpy
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


def BaseDetector_test():
    detector = BaseDetector()
    assert detector is not None
    assert detector.defaultSettings() == {}


def BRISKDetectorSettings_test():
    settings = BRISKDetectorSettings()
    assert settings is not None
    default_settings = {'thresh': 10, 'octaves': 0, 'patternScale': 1.0}
    test_settings = {'thresh': 11, 'octaves': 0, 'patternScale': 3.0}
    assert settings.exportSettings() == default_settings
    settings.importSettings(test_settings)
    assert settings.exportSettings() == test_settings
    settings.dump()


def BRISKDetector_test():
    detector = BRISKDetector()
    assert detector is not None
    img = cv2.imread(TEST_IMAGE_PATH)
    keypoints = detector.detect(img)
    assert keypoints is not None
    assert isinstance(keypoints[0], type(cv2.KeyPoint()))
    res = detector.compute(img, keypoints)
    assert res is not None
    assert len(res[0]) == len(keypoints)
    assert res[1] is not None
    assert isinstance(res[1], numpy.ndarray)
    res2 = detector.detectAndCompute(img)
    assert res2 is not None
    assert len(res2[0]) == len(res[0])
    assert numpy.array_equal(res2[1], res[1])


def ORBDetectorSettings_test():
    settings = ORBDetectorSettings()
    assert settings is not None
    default_settings = {'features': 500, 'scaleFactor': 1.1, 'nlevels': 8}
    test_settings = {'features': 1000, 'scaleFactor': 1.1, 'nlevels': 4}
    assert settings.exportSettings() == default_settings
    settings.importSettings(test_settings)
    assert settings.exportSettings() == test_settings
    settings.dump()


def ORBDetector_test():
    detector = ORBDetector()
    assert detector is not None
    img = cv2.imread(TEST_IMAGE_PATH)
    keypoints = detector.detect(img)
    assert keypoints is not None
    assert isinstance(keypoints[0], type(cv2.KeyPoint()))
    res = detector.compute(img, keypoints)
    assert res is not None
    assert len(res[0]) == len(keypoints)
    assert res[1] is not None
    assert isinstance(res[1], numpy.ndarray)
    res2 = detector.detectAndCompute(img)
    assert res2 is not None
    assert len(res2[0]) == len(res[0])
    assert numpy.array_equal(res2[1], res[1])


def SURFDetectorSettings_test():
    settings = SURFDetectorSettings()
    assert settings is not None
    default_settings = {'threshold': 100}
    test_settings = {'threshold': 200}
    assert settings.exportSettings() == default_settings
    settings.importSettings(test_settings)
    assert settings.exportSettings() == test_settings
    settings.dump()


def SURFDetector_test():
    detector = SURFDetector()
    assert detector is not None
    img = cv2.imread(TEST_IMAGE_PATH)
    keypoints = detector.detect(img)
    assert keypoints is not None
    assert isinstance(keypoints[0], type(cv2.KeyPoint()))
    res = detector.compute(img, keypoints)
    assert res is not None
    assert len(res[0]) == len(keypoints)
    assert res[1] is not None
    assert isinstance(res[1], numpy.ndarray)
    res2 = detector.detectAndCompute(img)
    assert res2 is not None
    assert len(res2[0]) == len(res[0])
    assert numpy.array_equal(res2[1], res[1])


def mahotasSURFDetectorSettings_test():
    settings = mahotasSURFDetectorSettings()
    assert settings is not None
    default_settings = {'octaves': 4, 'scales': 6, 'init_step_size': 1,
                        'threshold': 0.1, 'max_points': 2000, 'is_integral': False}
    test_settings = {'octaves': 2, 'scales': 10, 'init_step_size': 1,
                     'threshold': 0.5, 'max_points': 5000, 'is_integral': False}
    assert settings.exportSettings() == default_settings
    settings.importSettings(test_settings)
    assert settings.exportSettings() == test_settings
    settings.dump()


def mahotasSURFDetector_test():
    detector = mahotasSURFDetector()
    assert detector is not None
    img = cv2.imread(TEST_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
    keypoints = detector.detect(img)
    assert keypoints is not None
    assert isinstance(keypoints[0], type(cv2.KeyPoint()))
    res = detector.compute(img, keypoints)
    assert res is not None
    assert len(res[0]) == len(keypoints)
    assert res[1] is not None
    assert isinstance(res[1], numpy.ndarray)
    res2 = detector.detectAndCompute(img)
    assert res2 is not None
    assert len(res2[0]) == len(res[0])
    assert res2[1].shape == res[1].shape
