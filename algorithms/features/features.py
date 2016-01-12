from biomio.algorithms.algorithms.cvtools.effects import grayscaleAndEqualize, grayscale
from biomio.algorithms.algorithms.images.self_quotient_image import self_quotient_image
from biomio.algorithms.algorithms.images.colour_tools import hsv_values_extraction
from biomio.algorithms.algorithms.features.detectors import BaseDetector
import cv2


class BaseDecorator(BaseDetector):
    def __init__(self, detector):
        BaseDetector.__init__(self)
        self._detector = detector


class FeatureDetector(BaseDecorator):
    def __init__(self, detector):
        BaseDecorator.__init__(self, detector)

    def detect(self, image, mask=None):
        fea_image = dict()
        if image is None:
            return fea_image
        fea_image['data'] = image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        maskimg = None
        if mask is not None:
            maskimg = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        keypoints = self._detector.detect(gray, maskimg)
        fea_image['keypoints'] = keypoints
        return fea_image

    def detectAndCompute(self, image, mask=None):
        fea_image = dict()
        if image is None:
            return fea_image
        fea_image['data'] = image
        gray = grayscale(self_quotient_image(hsv_values_extraction(image)))
        # gray = grayscaleAndEqualize(image)
        maskimg = None
        if mask is not None:
            maskimg = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self._detector.detectAndCompute(gray, maskimg)
        fea_image['keypoints'] = keypoints
        fea_image['descriptors'] = descriptors
        return fea_image

    def compute(self, image, keypoints):
        fea_image = dict()
        if image is None:
            return fea_image
        fea_image['data'] = image
        gray = grayscaleAndEqualize(image)
        keypoints, descriptors = self._detector.compute(gray, keypoints)
        fea_image['keypoints'] = keypoints
        fea_image['descriptors'] = descriptors
        return fea_image
