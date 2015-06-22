from __future__ import absolute_import
import logger
from biomio.algorithms.algorithms.features.detectors import (BRISKDetector, ORBDetector,
                                           BRISKDetectorSettings, ORBDetectorSettings)
from biomio.algorithms.algorithms.features.classifiers import (getROIImage, RectsFiltering)
from biomio.algorithms.algorithms.recognition.features import (FeatureDetector,
                                             BRISKDetectorType, ORBDetectorType)


LSHashType = 0
NearPyHashType = 1


class KODSettings:
    """
    Keypoints Object Detector's Settings class
    """
    neighbours_distance = 1.0
    detector_type = BRISKDetectorType
    brisk_settings = BRISKDetectorSettings()
    orb_settings = ORBDetectorSettings()
    probability = 25.0

    def exportSettings(self):
        info = dict()
        info['Neighbours Distance'] = self.neighbours_distance
        info['Probability'] = self.probability
        settings = dict()
        if self.detector_type == BRISKDetectorType:
            info['Detector Type'] = 'BRISK'
            settings['Thresh'] = self.brisk_settings.thresh
            settings['Octaves'] = self.brisk_settings.octaves
            settings['Pattern Scale'] = self.brisk_settings.patternScale
        elif self.detector_type == ORBDetectorType:
            info['Detector Type'] = 'ORB'
            settings['Number of features'] = self.orb_settings.features
            settings['Scale Factor'] = self.orb_settings.scaleFactor
            settings['Number of levels'] = self.orb_settings.nlevels
        info['Detector Settings'] = settings
        return info

    def importSettings(self, settings):
        self.neighbours_distance = settings['Neighbours Distance']
        self.probability = settings['Probability']
        detector = settings.get('Detector Settings', dict())
        if settings.get('Detector Type') == 'BRISK':
            self.detector_type = BRISKDetectorType
            self.brisk_settings.thresh = detector['Thresh']
            self.brisk_settings.octaves = detector['Octaves']
            self.brisk_settings.patternScale = detector['Pattern Scale']
        elif settings.get('Detector Type') == 'ORB':
            self.detector_type = ORBDetectorType
            self.orb_settings.features = detector['Number of features']
            self.orb_settings.scaleFactor = detector['Scale Factor']
            self.orb_settings.nlevels = detector['Number of levels']

    def dump(self):
        logger.algo_logger.info('Keypoints Objects Detectors Settings')
        logger.algo_logger.info('Neighbours Distance: %f' % self.neighbours_distance)
        logger.algo_logger.info('Probability: %f' % self.probability)
        logger.algo_logger.info('Detector Type: %s' % self.detector_type)
        logger.algo_logger.info('BRISK Detector Settings')
        logger.algo_logger.info('   Thresh: %d' % self.brisk_settings.thresh)
        logger.algo_logger.info('   Octaves: %d' % self.brisk_settings.octaves)
        logger.algo_logger.info('   Pattern Scale: %f' % self.brisk_settings.patternScale)
        logger.algo_logger.info('ORB Detector Settings')
        logger.algo_logger.info('   Number of features: %d' % self.orb_settings.features)
        logger.algo_logger.info('   Scale Factor: %f' % self.orb_settings.scaleFactor)
        logger.algo_logger.info('   Number of levels: %d' % self.orb_settings.nlevels)


def identifying(fn):
    def wrapped(self, data):
        logger.algo_logger.info("Identifying...")
        res = None
        if self.data_detect(self, data):
            if data is not None:
                res = fn(self, data)
        logger.algo_logger.info("Identifying finished.")
        return res

    return wrapped


def verifying(fn):
    def wrapped(self, data):
        logger.algo_logger.info("Verifying...")
        res = False
        if self.data_detect(data):
            if data is not None:
                res = fn(self, data)
        logger.algo_logger.info("Verifying finished.")
        return res

    return wrapped


class KeypointsObjectDetector:
    kodsettings = KODSettings()

    def __init__(self):
        self._hash = None
        self._cascadeROI = None
        self._detector = None
        self._eyeROI = None
        self._use_roi = True
        self._last_error = ""

    def threshold(self):
        return self.kodsettings.probability

    def last_error(self):
        return self._last_error

    def setUseROIDetection(self, use):
        self._use_roi = use

    def addSource(self, data):
        self._last_error = ""
        logger.algo_logger.info("Training started...")
        logger.algo_logger.info(data['path'])
        if self.data_detect(data):
            self.update_hash(data)
        logger.algo_logger.info("Training finished.")

    def addSources(self, data_list):
        for data in data_list:
            self.addSource(data)

    def importSources(self, data):
        logger.algo_logger.info("Detector cannot import sources.")

    def exportSources(self):
        logger.algo_logger.info("Detector cannot export sources.")

    def importSettings(self, settings):
        logger.algo_logger.info("Detector cannot import settings.")

    def exportSettings(self):
        logger.algo_logger.info("Detector cannot export settings.")

    @identifying
    def identify(self, data):
        logger.algo_logger.info("Detector doesn't support image identification.")

    @verifying
    def verify(self, data):
        logger.algo_logger.info("Detector doesn't support image verification.")

    def detect(self, data):
        logger.algo_logger.info("Detector doesn't support image detection.")

    def data_detect(self, data):
        # ROI detection
        if self._use_roi:
            img, rect = self._cascadeROI.detectAndJoinWithRotation(data['data'], False, RectsFiltering)
            data['data'] = img
            if len(rect) <= 0:
                logger.algo_logger.info("Face ROI wasn't found.")
                self._last_error = "Face ROI wasn't found."
                return False
            print rect
            # ROI cutting
            data['roi'] = getROIImage(data['data'], rect)
        else:
            data['roi'] = data['data']
        # Keypoints detection
        detector = FeatureDetector()
        if self.kodsettings.detector_type is BRISKDetectorType:
            brisk_detector = BRISKDetector(self.kodsettings.brisk_settings.thresh,
                                           self.kodsettings.brisk_settings.octaves,
                                           self.kodsettings.brisk_settings.patternScale)
            detector.set_detector(brisk_detector)
        else:
            orb_detector = ORBDetector(self.kodsettings.orb_settings.features,
                                       self.kodsettings.orb_settings.scaleFactor,
                                       self.kodsettings.orb_settings.nlevels)
            detector.set_detector(orb_detector)
        try:
            obj = detector.detectAndComputeImage(data['roi'])
        except Exception as err:
            logger.algo_logger.debug(err.message)
            self._last_error = err.message
            return False
        data['keypoints'] = obj['keypoints']
        data['descriptors'] = obj['descriptors']
        if data['descriptors'] is None:
            data['descriptors'] = []
        return self._detect(data, detector)

    def _detect(self, data, detector):
        return True

    def update_hash(self, data):
        logger.algo_logger.info("The hash does not need to be updated!")

    def update_database(self):
        logger.algo_logger.info("The database does not need to be updated!")
