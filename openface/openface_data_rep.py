from biomio.algorithms.cascades.detectors import RotatedCascadesDetector, loadScript
from biomio.algorithms.flows.ialgorithm import IAlgorithm
from biomio.algorithms.logger import logger
import openface
import time
import cv2

class OpenFaceDataRepresentation(IAlgorithm):
    """
    Settings:
    {
        'dlibFacePredictor': dlib Face Predictor object
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
        self._net = openface.TorchNeuralNet(settings.get('networkModel'), settings.get('imgDim'))
        self._detector = RotatedCascadesDetector(
            loadScript("main_rotation_haarcascade_face_eyes.json", True), loadScript(""))

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("OpenFaceDataRepresentation::apply")
        logger.debug(data)
        logger.debug("===================================")
        bgrImg = cv2.imread(data.get('path'))
        if bgrImg is None:
            # TODO: Write Error handler
            raise Exception("Unable to load image: {}".format(data.get('path')))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
        if self._detector is not None:
            rgbImg = self._detector.detect(rgbImg)[0]

        bb = self._align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            # TODO: Write Error handler
            raise Exception("Unable to find a face: {}".format(data.get('path')))

        start = time.time()
        alignedFace = self._align.align(self._settings.get('imgDim'), rgbImg, bb,
                                        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            # TODO: Write Error handler
            raise Exception("Unable to align image: {}".format(data.get('path')))
        logger.debug("Face alignment for {} took {} seconds.".format(data.get('path'), time.time() - start))

        start = time.time()
        rep = self._net.forward(alignedFace)
        logger.debug("OpenFace forward pass for {} took {} seconds.".format(data.get('path'), time.time() - start))
        data.update({'rep': rep})
        return data
