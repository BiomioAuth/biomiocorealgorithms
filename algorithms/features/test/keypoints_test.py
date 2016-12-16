from ..keypoints import identifying, verifying, KeypointsObjectDetector
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.jpg")


class TestDetector:
    def __init__(self):
        self._sources_preparing = True
        pass

    def _prepare_sources(self, data):
        pass

    def data_detect(self, data):
        return True

    @identifying
    def test_identify(self, data):
        return data

    @verifying
    def test_verify(self, data):
        return data


def identifying_test():
    detector = TestDetector()
    assert detector is not None
    assert detector.test_identify({}) == {}


def verifying_test():
    detector = TestDetector()
    assert detector is not None
    assert detector.test_verify({}) == {}


def KeypointsObjectDetector_test():
    img = cv2.imread(TEST_IMAGE_PATH)
    detector = KeypointsObjectDetector()
    assert detector is not None
    assert detector.threshold() == 25.0
    assert detector.last_error() == ""
    detector.setUseROIDetection(False)
    assert detector.addSource({'path': TEST_IMAGE_PATH, 'data': img})
    assert detector.addSources([{'path': TEST_IMAGE_PATH, 'data': img}, {'path': TEST_IMAGE_PATH, 'data': img},
                                {'path': TEST_IMAGE_PATH, 'data': img}, {'path': TEST_IMAGE_PATH, 'data': img}]) == 4
    detector.importSources({})
    detector.exportSources()
    detector.importSettings({})
    detector.exportSettings()
    detector.identify({'path': TEST_IMAGE_PATH, 'data': img})
    detector.verify({'path': TEST_IMAGE_PATH, 'data': img})
    detector.detect({'path': TEST_IMAGE_PATH, 'data': img})
    assert detector.data_detect({'path': TEST_IMAGE_PATH, 'data': img})
    detector.update_hash({})
    detector.update_database()
