from ..general.base import IAlgorithm
from ...logger import logger
import openface
import time
import cv2


OUTER_EYES_AND_NOSE = openface.AlignDlib.OUTER_EYES_AND_NOSE
INNER_EYES_AND_BOTTOM_LIP = openface.AlignDlib.INNER_EYES_AND_BOTTOM_LIP

DLIB_PREDICTOR_V1 = 1
DLIB_PREDICTOR_V2 = 2


class DLibFaceDetectionAlgorithm(IAlgorithm):
    """
    Settings:
    {
        'dlibFacePredictor': dlib Face Predictor object,
        'landmarkIndices': Type of landmark indices,
        'predictorVersion': version of DLib Face Predictor,
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
        self._settings = settings
        self._align = openface.AlignDlib(settings.get('dlibFacePredictor'))
        self._landmarkIndices = settings.get('landmarkIndices', INNER_EYES_AND_BOTTOM_LIP)
        self._predictor_version = settings.get('predictorVersion', DLIB_PREDICTOR_V2)
        self._error_handler = settings.get('error_handler', None)

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("DLibFaceDetectionAlgorithm::apply")
        logger.debug(data)
        logger.debug("===================================")
        rgbImg = cv2.cvtColor(data.get('img'), cv2.COLOR_BGR2RGB)

        bb = self._align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            return self._process_error(data, "DLibFaceDetectionAlgorithm::Unable to find a face: {}"
                                       .format(data.get('path')))
        start = time.time()
        alignedFace = self._align.align(self._settings.get('imgDim'), rgbImg, bb,
                                        landmarkIndices=self._landmarkIndices, version=self._predictor_version)
        if alignedFace is None:
            return self._process_error(data, "DLibFaceDetectionAlgorithm::Unable to align image: {}"
                                       .format(data.get('path')))
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
