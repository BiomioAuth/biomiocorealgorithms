from ..algorithms.cascades.detectors import RotatedCascadesDetector, loadScript
from base import IAlgorithm
from ..logger import logger


class RotationDetectionAlgorithm(IAlgorithm):
    """
    Input:
    {
        'img': numpy.ndarray of the image file
    }
    Output:
    {
        'img': numpy.ndarray of the image file
    }
    """
    def __init__(self):
        self._detector = RotatedCascadesDetector(
            loadScript("main_rotation_haarcascade_face_eyes.json", True), loadScript(""))

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("RotationDetectionAlgorithm::apply")
        logger.debug(data)
        logger.debug("===================================")
        img = data.get('img', None)
        if img is not None and self._detector is not None:
            img = self._detector.detect(img)[0]
        data.update({'img': img})
        return data
