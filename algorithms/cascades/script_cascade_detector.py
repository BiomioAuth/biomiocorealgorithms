from classifiers import CascadeROIDetector
from strategies import StrategyFactory
from tools import skipEmptyRectangles
import os


MULTIPROCESSING_ENABLED = False


def task_process(data):
    classifier = CascadeROIDetector()
    classifier.classifierSettings.importSettings(data['settings'])
    classifier.add_cascade(data['cascade'])
    return {data['name']: classifier.detect(data['image'], True)}


class ScriptStage:
    def __init__(self):
        self.name = "default"
        self.type = "main"
        self.stages = []
        self.strategy = None


class ScriptTask:
    def __init__(self):
        self.name = "default"
        self.type = "task"
        self.cascade = None
        self.settings = {}

    def serialize(self):
        return {'name': self.name,
                'type': self.type,
                'cascade': self.cascade,
                'settings': self.settings}


class ScriptCascadeDetector:
    def __init__(self, detect_script, preload_cascades=False):
        self._stage = None
        self._tasks = {}
        if len(detect_script.keys()) > 0:
            self._stage, self._tasks = self.init_stage(detect_script, preload_cascades)
        self._backup = {}

    @staticmethod
    def init_stage(detect_script, init_cascade=False):
        tasks = {}
        stage = ScriptStage()
        stage.type = detect_script["type"]
        stage.name = detect_script["name"]
        stage.strategy = StrategyFactory.get(detect_script["strategy"])
        if detect_script["type"] == "main":
            stages = detect_script["action"]
            for sub in stages:
                substage, add_tasks = ScriptCascadeDetector.init_stage(sub, init_cascade)
                stage.stages.append(substage)
                tasks.update(add_tasks)
        else:
            settings_list = []
            if isinstance(detect_script["action"]["settings"], dict):
                settings_list = [detect_script["action"]["settings"]]
            elif isinstance(detect_script["action"]["settings"], list):
                settings_list = detect_script["action"]["settings"]
            cascades = detect_script["action"]["cascades"]
            for cascade in cascades:
                subname = os.path.split(cascade)[1]
                inx = 0
                for settings in settings_list:
                    task = ScriptTask()
                    task.name = "{}/{}/{}".format(stage.name, subname, inx)
                    if init_cascade:
                        classifier = CascadeROIDetector()
                        classifier.classifierSettings.importSettings(settings)
                        classifier.add_cascade(cascade)
                        task.cascade = classifier
                    else:
                        task.cascade = cascade
                    task.settings = settings
                    stage.stages.append(task)
                    tasks[task.name] = task
                    inx += 1
        return stage, tasks

    def detect(self, image):
        self._backup = {}
        if MULTIPROCESSING_ENABLED:
            import multiprocessing as mp
            tasks_list = []
            for key, task in self._tasks.iteritems():
                data = task.serialize()
                data.update({'image': image})
                tasks_list.append(data)
            pool = mp.Pool(processes=len(tasks_list))
            lrects = pool.map(task_process, tasks_list)
            for rect in lrects:
                for key, task_result in rect.iteritems():
                    self._backup[key] = task_result
            pool.close()
        else:
            for key, task in self._tasks.iteritems():
                self._backup[key] = self.apply_task(image, task)

        if self._stage:
            return image, self.apply_stage(image, self._stage)
        return image, []

    @staticmethod
    def apply_task(image, task):
        if isinstance(task.cascade, CascadeROIDetector):
            classifier = task.cascade
        else:
            classifier = CascadeROIDetector()
            classifier.classifierSettings.importSettings(task.settings)
            classifier.add_cascade(task.cascade)
        return classifier.detect(image, True)

    def apply_stage(self, image, stage):
        if self._backup.get(stage.name, None) is not None:
            return self._backup[stage.name]
        rects = []
        for s in stage.stages:
            rects += self.apply_stage(image, s)
        new_rects = skipEmptyRectangles(rects)
        result = stage.strategy.apply(new_rects)
        self._backup[stage.name] = result
        return result
