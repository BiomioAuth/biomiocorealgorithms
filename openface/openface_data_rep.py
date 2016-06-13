from biomio.algorithms.cascades.detectors import RotatedCascadesDetector, loadScript
from biomio.algorithms.flows.base import IAlgorithm
from biomio.algorithms.logger import logger
import openface
import time
import cv2


OUTER_EYES_AND_NOSE = openface.AlignDlib.OUTER_EYES_AND_NOSE
INNER_EYES_AND_BOTTOM_LIP = openface.AlignDlib.INNER_EYES_AND_BOTTOM_LIP

DLIB_PREDICTOR_V1 = 1
DLIB_PREDICTOR_V2 = 2


class OpenFaceDataRepresentation(IAlgorithm):
    """
    Settings:
    {
        'dlibFacePredictor': dlib Face Predictor object
        'landmarkIndices': Type of landmark indices
        'predictorVersion': version of DLib Face Predictor
        'networkModel': Torch neural network model
        'imgDim': image dimension
    }
    Input:
    {
        'path': abstract path to the image file
    }
    Output:
    {
        'path': abstract path to the image file
        'rep': OpenFace image representation
    }
    """
    def __init__(self, settings):
        self._settings = settings
        self._align = openface.AlignDlib(settings.get('dlibFacePredictor'))
        self._landmarkIndices = settings.get('landmarkIndices', INNER_EYES_AND_BOTTOM_LIP)
        self._predictor_version = settings.get('predictorVersion', DLIB_PREDICTOR_V2)
        self._net = openface.TorchNeuralNet(settings.get('networkModel'), settings.get('imgDim'))
        self._detector = RotatedCascadesDetector(
            loadScript("main_rotation_haarcascade_face_eyes.json", True), loadScript(""))
        self._error_handler = settings.get('error_handler', None)

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("OpenFaceDataRepresentation::apply")
        logger.debug(data)
        logger.debug("===================================")
        bgrImg = cv2.imread(data.get('path'))
        if bgrImg is None:
            return self._process_error(data, "Unable to load image: {}".format(data.get('path')))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
        if self._detector is not None:
            rgbImg = self._detector.detect(rgbImg)[0]

        bb = self._align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            return self._process_error(data, "Unable to find a face: {}".format(data.get('path')))

        start = time.time()
        alignedFace = self._align.align(self._settings.get('imgDim'), rgbImg, bb,
                                        landmarkIndices=self._landmarkIndices, version=self._predictor_version)
        if alignedFace is None:
            return self._process_error(data, "Unable to align image: {}".format(data.get('path')))
        logger.debug("Face alignment for {} took {} seconds.".format(data.get('path'), time.time() - start))

        start = time.time()
        rep = self._net.forward(alignedFace)
        logger.debug("OpenFace forward pass for {} took {} seconds.".format(data.get('path'), time.time() - start))
        data.update({'rep': rep})
        return data

    def clean(self):
        self._net.exit()

    def _process_error(self, data, message):
        if self._error_handler is not None:
            self._error_handler({
                'path': data['path'],
                'message': message
            })
            data.update({'rep': []})
            return data
        else:
            raise Exception(message)
