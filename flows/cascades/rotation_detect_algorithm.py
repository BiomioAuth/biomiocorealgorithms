from ...algorithms.cascades.detectors import RotatedCascadesDetector, loadScript
from ..general.decorators import algorithm_header
from ..general.base import IAlgorithm
from ...logger import logger


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

    @algorithm_header
    def apply(self, data):
        img = data.get('img', None)
        if img is not None and self._detector is not None:
            img = self._detector.detect(img)[0]
        data.update({'img': img})
        return data
