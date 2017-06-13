from ...algorithms.cascades.scripts_detectors import CascadesDetectionInterface
from ...algorithms.cascades.detectors import loadScript, getROIImage
from ..general.decorators import algorithm_header
from ..general.base import IAlgorithm
from ...logger import logger
import time
import cv2


class CascadesFaceDetectionAlgorithm(IAlgorithm):
    """
    Settings:
    {
        'imgDim': image dimension
    }
    Input:
    {
        'img': numpy.ndarray of the image file,
        'path': abstract path to the image file
    }
    Output:
    {
        'img': numpy.ndarray of the image file
    }
    """
    def __init__(self, settings):
        self._imgDim = settings.get('imgDim', 96)
        self._error_handler = settings.get('error_handler', None)
        self._roi_detector = CascadesDetectionInterface(loadScript("main_haarcascade_face_size.json", True))

    @algorithm_header
    def apply(self, data):
        start = time.time()
        roi_data = self._roi_detector.detect(data.get('img'))
        alignedFace = getROIImage(roi_data[0], roi_data[1][0])
        if alignedFace is not None:
            if self._imgDim is not None and self._imgDim > 0:
                alignedFace = cv2.resize(alignedFace, (self._imgDim, self._imgDim), interpolation=cv2.INTER_LANCZOS4)
                alignedFace = cv2.cvtColor(alignedFace, cv2.COLOR_BGR2RGB)
        else:
            return self._process_error(data, "Unable to find a face: {}".format(data.get('path')))
        logger.debug("Face alignment for {} took {} seconds.".format(data.get('path'), time.time() - start))
        data.update({'img': alignedFace})
        return data

    def _process_error(self, data, message):
        if self._error_handler is not None:
            self._error_handler({
                'path': data['path'],
                'message': message
            })
        data.update({'img': None})
        return data
