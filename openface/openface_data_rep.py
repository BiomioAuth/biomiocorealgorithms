from biomio.algorithms.flows import AlgorithmFlow
from biomio.algorithms.logger import logger
import openface
import time
import cv2


OUTER_EYES_AND_NOSE = openface.AlignDlib.OUTER_EYES_AND_NOSE
INNER_EYES_AND_BOTTOM_LIP = openface.AlignDlib.INNER_EYES_AND_BOTTOM_LIP

DLIB_PREDICTOR_V1 = 1
DLIB_PREDICTOR_V2 = 2

FACE_ROTATION_STAGE = "flows::face_rotation_stage"
FACE_ALIGNMENT_STAGE = "flows::face_alignment_stage"


class OpenFaceDataRepresentation(AlgorithmFlow):
    """
    Settings:
    {
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
        AlgorithmFlow.__init__(self)
        self._settings = settings
        self._net = openface.TorchNeuralNet(settings.get('networkModel'), settings.get('imgDim'))
        self._error_handler = settings.get('error_handler', None)

    def faceRotationStage(self):
        return self._stages.get(FACE_ROTATION_STAGE, None)

    def setFaceRotationStage(self, stage):
        if stage is not None:
            self._stages[FACE_ROTATION_STAGE] = stage

    def faceAlignmentStage(self):
        return self._stages.get(FACE_ALIGNMENT_STAGE, None)

    def setFaceAlignmentStage(self, stage):
        if stage is not None:
            self._stages[FACE_ALIGNMENT_STAGE] = stage

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("OpenFaceDataRepresentation::apply")
        logger.debug(data)
        logger.debug("===================================")
        bgrImg = cv2.imread(data.get('path'))
        if bgrImg is None:
            return self._process_error(data, "Unable to load image: {}".format(data.get('path')))
        if self.faceRotationStage() is not None:
            bgrImg = self.faceRotationStage().apply({'img': bgrImg})['img']

        start = time.time()
        alignData = data.copy()
        alignData.update({'img': bgrImg})
        alignedFace = self.faceAlignmentStage().apply(alignData)['img']
        logger.debug("General Face alignment for {} took {} seconds.".format(data.get('path'), time.time() - start))
        if alignedFace is None:
            return self._process_error(data, "General::Unable to align image: {}".format(data.get('path')))

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
