from classifiers import CascadeROIDetector
from strategies import StrategyFactory
from tools import skipEmptyRectangles, isRectangle
import cv2

class DetectorStage:
    def __init__(self):
        self.type = "main"
        self.stages = []
        self.classifier = None
        self.strategy = None


class CascadesDetectionInterface:
    def __init__(self, detect_script, template_script=dict()):
        self._stage = None
        if len(detect_script.keys()) > 0:
            self._stage = self._init_stage(detect_script)
        self._template = None
        if len(template_script.keys()) > 0:
            self._template = self._init_stage(template_script)

    def _init_stage(self, detect_script):
        stage = DetectorStage()
        stage.type = detect_script["type"]
        stage.strategy = StrategyFactory.get(detect_script["strategy"])
        if detect_script["type"] == "main":
            stages = detect_script["action"]
            for sub in stages:
                stage.stages.append(self._init_stage(sub))
        else:
            classifier = CascadeROIDetector()
            classifier.classifierSettings.importSettings(detect_script["action"]["settings"])
            cascades = detect_script["action"]["cascades"]
            for cascade in cascades:
                classifier.add_cascade(cascade)
            stage.classifier = classifier
        return stage

    def detect(self, image):
        temp = []
        if self._template:
            temp = self._apply_stage(image, self._template)
        if self._stage:
            return image, self._apply_stage(image, self._stage, temp)
        return image, []

    def _apply_stage(self, image, stage, template=[]):
        rects = []
        if stage.type == "main":
            for s in stage.stages:
                rects += self._apply_stage(image, s)
        else:
            rects = stage.classifier.detect(image, True)
        new_rects = skipEmptyRectangles(rects)
        return stage.strategy.apply(new_rects, template)


class RotatedCascadesDetector(CascadesDetectionInterface):
    def __init__(self, rotate_script, detect_script, template_script=dict()):
        CascadesDetectionInterface.__init__(self, detect_script, template_script)
        self._rotation = None
        if len(rotate_script.keys()) > 0:
            self._rotation = self._init_stage(rotate_script)

    def detect(self, image):
        img = self._apply_rotate(image)
        return CascadesDetectionInterface.detect(self, img)

    def _rotate(self, image):
        rows = image.shape[0]
        cols = image.shape[1]
        M = cv2.getRotationMatrix2D((cols/2.0, cols/2.0), 90, 1)
        img = cv2.warpAffine(image, M, (rows, cols))
        return img

    def _apply_rotate(self, image):
        if self._rotation:
            img = image
            img2 = self._rotate(img)
            img3 = self._rotate(img2)
            img4 = self._rotate(img3)
            d = dict()
            rects = []
            if len(self._rotation.stages) > 1:
                r1 = []
                r2 = []
                r3 = []
                r4 = []
                for stage in self._rotation.stages:
                    lr1 = self._apply_stage(img, stage)
                    r1 += lr1
                    for lr in lr1:
                        d[str(lr)] = img
                    lr2 = self._apply_stage(img2, stage)
                    r2 += lr2
                    for lr in lr2:
                        d[str(lr)] = img2
                    lr3 = self._apply_stage(img3, stage)
                    r3 += lr3
                    for lr in lr3:
                        d[str(lr)] = img3
                    lr4 = self._apply_stage(img4, stage)
                    r4 += lr4
                    for lr in lr4:
                        d[str(lr)] = img4
                if isRectangle(r1[0]):
                    rects.append(skipEmptyRectangles(r1))
                if isRectangle(r2[0]):
                    rects.append(skipEmptyRectangles(r2))
                if isRectangle(r3[0]):
                    rects.append(skipEmptyRectangles(r3))
                if isRectangle(r4[0]):
                    rects.append(skipEmptyRectangles(r4))
            else:
                stage = self._rotation.stages[0]
                r1 = self._apply_stage(img, stage)
                rects += r1
                for lr in r1:
                    d[str(lr)] = img
                r2 = self._apply_stage(img2, stage)
                rects += r2
                for lr in r2:
                    d[str(lr)] = img2
                r3 = self._apply_stage(img3, stage)
                rects += r3
                for lr in r3:
                    d[str(lr)] = img3
                r4 = self._apply_stage(img4, stage)
                rects += r4
                for lr in r4:
                    d[str(lr)] = img4
                rects = skipEmptyRectangles(rects)
            d[str([])] = image
            rect = self._rotation.strategy.apply(rects)
            return d[str(rect[0])]
        return image
