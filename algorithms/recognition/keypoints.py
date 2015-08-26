from __future__ import absolute_import
from biomio.algorithms.algorithms.features import (constructDetector, constructSettings, BRISKDetectorType)
from biomio.algorithms.algorithms.cascades.classifiers import RectsFiltering
from biomio.algorithms.algorithms.cascades.tools import getROIImage
from biomio.algorithms.algorithms.features.features import (FeatureDetector)
from biomio.algorithms.algorithms.cascades.roi_optimal import OptimalROIDetector, OptimalROIDetectorSAoS
import logger


LSHashType = 0
NearPyHashType = 1


class KODSettings:
    """
    Keypoints Object Detector's Settings class
    """
    neighbours_distance = 1.0
    detector_type = BRISKDetectorType
    settings = None
    probability = 25.0

    def exportSettings(self):
        return {
            'Neighbours Distance': self.neighbours_distance,
            'Probability': self.probability,
            'Detector Type': self.detector_type,
            'Detector Settings': self.settings.exportSettings()
        }

    def importSettings(self, settings):
        self.neighbours_distance = settings['Neighbours Distance']
        self.probability = settings['Probability']
        self.detector_type = settings.get('Detector Type')
        self.settings = constructSettings(self.detector_type)
        self.settings.importSettings(settings.get('Detector Settings', dict()))

    def dump(self):
        logger.algo_logger.info('Keypoints Objects Detectors Settings')
        logger.algo_logger.info('Neighbours Distance: %f' % self.neighbours_distance)
        logger.algo_logger.info('Probability: %f' % self.probability)
        logger.algo_logger.info('Detector Type: %s' % self.detector_type)
        self.settings.dump()


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


def identifying(fn):
    def wrapped(self, data):
        logger.algo_logger.debug("Identifying...")
        res = None
        if self.data_detect(self, data):
            if data is not None:
                res = fn(self, data)
        logger.algo_logger.debug("Identifying finished.")
        return res
    return wrapped


def verifying(fn):
    def wrapped(self, data):
        logger.algo_logger.info("Verifying...")
        res = False
        if self._sources_preparing:
            self._prepare_sources([data])
        if self.data_detect(data):
            if data is not None:
                res = fn(self, data)
        logger.algo_logger.info("Verifying finished.")
        return res
    return wrapped


class KeypointsObjectDetector:
    kodsettings = KODSettings()

    def __init__(self):
        self._database = None
        self._cascadeROI = None
        self._detector = None
        self._eyeROI = None
        self._use_roi = True
        self._sources_preparing = False
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
            return True
        logger.algo_logger.info("Training finished.")
        return False

    def addSources(self, data_list):
        if self._sources_preparing:
            data_list = self._prepare_sources(data_list)
        count = 0
        for data in data_list:
            res = self.addSource(data)
            if res:
                count += 1
        return count

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
            detector = OptimalROIDetectorSAoS()
            detector.detect([data])
            data['roi'] = data['data']
        else:
            data['roi'] = data['data']
        # Keypoints detection
        detector = FeatureDetector(constructDetector(self.kodsettings.detector_type, self.kodsettings.settings))
        try:
            obj = detector.detectAndCompute(data['roi'])
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

    def _prepare_sources(self, data_list):
        self._use_roi = False
        detector = OptimalROIDetectorSAoS()
        data_list = detector.detect(data_list)
        return data_list

    def update_hash(self, data):
        logger.algo_logger.info("The hash does not need to be updated!")

    def update_database(self):
        logger.algo_logger.info("The database does not need to be updated!")
