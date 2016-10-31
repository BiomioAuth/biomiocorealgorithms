from ..cvtools import listToNumpy_ndarray
# from ...logger import logger
from mahotas.features import surf
import numpy
import cv2


class BaseDetector:
    def __init__(self):
        print self.__class__
        self._detector = None
        self._extractor = None

    def descriptorSize(self):
        logger.debug(self._detector.__dict__)
        return self._detector.size()

    def descriptorType(self):
        logger.debug(self._detector.__dict__)
        return self._detector.type()

    @staticmethod
    def defaultSettings():
        return dict()

    def detect(self, image, mask=None):
        return self._detector.detect(image, mask)

    def detectAndCompute(self, image, mask=None):
        if self._extractor is not None:
            keypoints = self._detector.detect(image, mask)
            return self._extractor.compute(image, keypoints)
        try:
            return self._detector.detectAndCompute(image, mask)
        except Exception as err:
            logger.debug(err.message)
            return None

    def compute(self, image, keypoints):
        if self._extractor is not None:
            return self._extractor.compute(image, keypoints)
        try:
            return self._detector.compute(image, keypoints)
        except Exception as err:
            logger.debug(err.message)
            return None


class BRISKDetectorSettings:
    thresh = 10
    octaves = 0
    patternScale = 1.0

    def exportSettings(self):
        return {
            'thresh': self.thresh,
            'octaves': self.octaves,
            'patternScale': self.patternScale
        }

    def importSettings(self, settings):
        if len(settings.keys()) > 0:
            self.thresh = settings['thresh']
            self.octaves = settings['octaves']
            self.patternScale = settings['patternScale']

    def dump(self):
        logger.debug('BRISK Detector Settings:')
        logger.debug('    Threshold: %f' % self.thresh)
        logger.debug('    Octaves: %f' % self.octaves)
        logger.debug('    Pattern Scale: %f' % self.patternScale)


class BRISKDetector(BaseDetector):
    def __init__(self, settings=BRISKDetectorSettings()):
        BaseDetector.__init__(self)
        self._detector = cv2.BRISK(thresh=settings.thresh,
                                   octaves=settings.octaves,
                                   patternScale=settings.patternScale)
        self._extractor = self._detector

    @staticmethod
    def defaultSettings():
        return {
            'thresh': 10,
            'octaves': 0,
            'scale': 1.0
        }


class ORBDetectorSettings:
    features = 500
    scaleFactor = 1.1
    nlevels = 8

    def exportSettings(self):
        return {
            'features': self.features,
            'scaleFactor': self.scaleFactor,
            'nlevels': self.nlevels
        }

    def importSettings(self, settings):
        if len(settings.keys()) > 0:
            self.features = settings['features']
            self.scaleFactor = settings['scaleFactor']
            self.nlevels = settings['nlevels']

    def dump(self):
        logger.debug('ORB Detector Settings:')
        logger.debug('    Features: %d' % self.features)
        logger.debug('    Scale Factor: %f' % self.scaleFactor)
        logger.debug('    Levels: %d' % self.nlevels)


class ORBDetector(BaseDetector):
    def __init__(self, settings=ORBDetectorSettings()):
        BaseDetector.__init__(self)
        self._detector = cv2.ORB(nfeatures=settings.features,
                                 scaleFactor=settings.scaleFactor,
                                 nlevels=settings.nlevels)
        self._extractor = self._detector

    @staticmethod
    def defaultSettings():
        return {
            'features': 500,
            'scaleFactor': 1.1,
            'nlevels': 8
        }


class SURFDetectorSettings:
    threshold = 100

    def exportSettings(self):
        return {
            'threshold': self.threshold
        }

    def importSettings(self, settings):
        if len(settings.keys()) > 0:
            self.threshold = settings['threshold']

    def dump(self):
        logger.debug('SURF Detector Settings:')
        logger.debug('    Threshold: %f' % self.threshold)


class SURFDetector(BaseDetector):
    def __init__(self, settings=SURFDetectorSettings()):
        BaseDetector.__init__(self)
        self._detector = cv2.SURF(hessianThreshold=settings.threshold)
        self._detector.extended = False
        self._extractor = self._detector


class mahotasSURFDetectorSettings:
    nr_octaves = 4
    nr_scales = 6
    initial_step_size = 1
    threshold = 0.1
    max_points = 2000
    is_integral = False

    def exportSettings(self):
        return {
            'octaves': self.nr_octaves,
            'scales': self.nr_scales,
            'init_step_size': self.initial_step_size,
            'threshold': self.threshold,
            'max_points': self.max_points,
            'is_integral': self.is_integral
        }

    def importSettings(self, settings):
        if len(settings.keys()) > 0:
            self.nr_octaves = settings['octaves']
            self.nr_scales = settings['scales']
            self.initial_step_size = settings['init_step_size']
            self.threshold = settings['threshold']
            self.max_points = settings['max_points']
            self.is_integral = settings['is_integral']

    def dump(self):
        logger.debug('Mahotas SURF Detector Settings:')
        logger.debug('    Octaves: %f' % self.nr_octaves)
        logger.debug('    Scales: %f' % self.nr_scales)
        logger.debug('    Initial Step Size: %f' % self.initial_step_size)
        logger.debug('    Threshold: %f' % self.threshold)
        logger.debug('    Max Points: %f' % self.max_points)
        logger.debug('    Integral: %d' % self.is_integral)


class mahotasSURFDetector(BaseDetector):
    def __init__(self, settings=mahotasSURFDetectorSettings()):
        BaseDetector.__init__(self)
        self._settings = settings
        self._filtered = True

    def type(self):
        return "mSurf"

    def size(self):
        return 64

    def detect(self, image, mask=None):
        keypoints = surf.interest_points(image, self._settings.nr_octaves, self._settings.nr_scales,
                                         self._settings.initial_step_size, self._settings.threshold,
                                         self._settings.max_points, self._settings.is_integral)
        if self._filtered:
            keypoints = mahotasSURFDetector._internal_keypoints_filter(image.shape, keypoints)
        return [mahotasSURFDetector.getKeyPoint(keypoint) for keypoint in keypoints]

    def detectAndCompute(self, image, mask=None):
        keypoints = surf.interest_points(image, self._settings.nr_octaves, self._settings.nr_scales,
                                         self._settings.initial_step_size, self._settings.threshold,
                                         self._settings.max_points, self._settings.is_integral)
        if self._filtered:
            keypoints = mahotasSURFDetector._internal_keypoints_filter(image.shape, keypoints)
        descriptors = surf.descriptors(image, keypoints, self._settings.is_integral, True)
        cvkeys = [mahotasSURFDetector.getKeyPoint(keypoint) for keypoint in keypoints]
        return cvkeys, listToNumpy_ndarray([mahotasSURFDetector.getDescriptor(d) for d in descriptors])

    def compute(self, image, keypoints):
        if keypoints is None or len(keypoints) == 0:
            return keypoints, []
        mkeys = [mahotasSURFDetector.getMahotasKeypoint(keypoint) for keypoint in keypoints]
        return keypoints, listToNumpy_ndarray([mahotasSURFDetector.getDescriptor(d) for d in
                                               surf.descriptors(image, mkeys, self._settings.is_integral, True)])

    @staticmethod
    def _internal_keypoints_filter(image_shape, keypoints):
        border = 31.0
        res = []
        for keypoint in keypoints:
            border_size = (border * keypoint[2]) / 2.0
            if (border_size <= keypoint[0] and (keypoint[0] + border_size) < image_shape[0] and
                        border_size <= keypoint[1] and (keypoint[1] + border_size) < image_shape[1]):
                res.append(keypoint)
        return res

    @staticmethod
    def getKeyPoint(keypoint):
        return cv2.KeyPoint(keypoint[1], keypoint[0], keypoint[2], keypoint[4], keypoint[3])

    @staticmethod
    def getMahotasKeypoint(keypoint):
        return [keypoint.pt[1], keypoint.pt[0], keypoint.size, keypoint.response, keypoint.angle]

    @staticmethod
    def getDescriptor(descriptor):
        return listToNumpy_ndarray(descriptor, numpy.float32)
