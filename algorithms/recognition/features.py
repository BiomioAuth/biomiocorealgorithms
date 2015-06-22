from biomio.algorithms.algorithms.features.detectors import (BRISKDetector, ORBDetector)
from biomio.algorithms.algorithms.features.matchers import Matcher, BruteForceMatcherType
from biomio.algorithms.algorithms.cvtools.effects import grayscaleAndEqualize
import numpy
import sys
import cv2


BRISKDetectorType = 'BRISK'
ORBDetectorType = 'ORB'
BRISKORBDetectorType = 'BRISK/ORB'


class FeatureDetector:
    def __init__(self, detector_type=ORBDetectorType):
        self._detector = None
        self._extractor = None
        if detector_type is BRISKDetectorType:
            self._detector = BRISKDetector()
            self._extractor = BRISKDetector.extractor()
        elif detector_type is ORBDetectorType:
            self._detector = ORBDetector()
            self._extractor = ORBDetector.extractor()
        self._matcher = Matcher(BruteForceMatcherType)

    def set_detector(self, detector):
        if detector is not None:
            self._detector = detector
            self._extractor = detector.extractor()

    def detect(self, filepath, maskpath=None):
        fea_image = dict()

        img = cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR)
        if img is None:
            print "Couldn't find the object image with the provided path."
            sys.exit()
        fea_image['data'] = img

        gray = grayscaleAndEqualize(img)
        mask = None
        if maskpath is not None:
            mask = cv2.imread(maskpath, cv2.CV_LOAD_IMAGE_GRAYSCALE)

        keypoints = self._detector.detect(gray, mask)
        fea_image['keypoints'] = keypoints
        return fea_image

    def detectImage(self, image, maskimage=None):
        fea_image = dict()
        if image is None:
            return fea_image

        fea_image['data'] = image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mask = None
        if maskimage is not None:
            mask = cv2.cvtColor(maskimage, cv2.COLOR_BGR2GRAY)

        keypoints = self._detector.detect(gray, mask)
        fea_image['keypoints'] = keypoints
        return fea_image

    def computeImage(self, image, keypoints):
        fea_image = dict()
        if image is None:
            return fea_image
        fea_image['data'] = image

        gray = grayscaleAndEqualize(image)
        keypoints, descriptors = self._extractor.compute(gray, keypoints)
        fea_image['keypoints'] = keypoints
        fea_image['descriptors'] = descriptors
        return fea_image

    def detectAndComputeImage(self, image, maskimage=None):
        fea_image = dict()
        if image is None:
            return fea_image
        fea_image['data'] = image

        gray = grayscaleAndEqualize(image)
        mask = None
        if maskimage is not None:
            mask = cv2.cvtColor(maskimage, cv2.COLOR_BGR2GRAY)

        keypoints = self._detector.detect(gray, mask)
        keypoints, descriptors = self._extractor.compute(gray, keypoints)
        fea_image['keypoints'] = keypoints
        fea_image['descriptors'] = descriptors
        return fea_image

    def detectAndCompute(self, filepath, maskpath=None):
        fea_image = dict()
        img = cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR)
        if img is None:
            print "Couldn't find the object image with the provided path."
            sys.exit()
        fea_image['data'] = img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = None
        if maskpath is not None:
            mask = cv2.imread(maskpath, cv2.CV_LOAD_IMAGE_GRAYSCALE)

        keypoints = self._detector.detect(gray, mask)
        keypoints, descriptors = self._extractor.compute(gray, keypoints)
        fea_image['keypoints'] = keypoints
        fea_image['descriptors'] = descriptors
        return fea_image

    def match(self, obj, scn):
        matches = self._matcher.knnMatch(obj['descriptors'], scn['descriptors'], k=2)

        #Apply ratio test
        good = []
        for m, n in matches:
            print str(m.imgIdx) + " " + str(m.distance) + " " + str(n.imgIdx) + " " + str(n.distance)
            if m.distance < 0.75 * n.distance:
                good.append([m])
                print 'true'

        # img1 = obj.image()
        # img2 = scn_feature.image()
