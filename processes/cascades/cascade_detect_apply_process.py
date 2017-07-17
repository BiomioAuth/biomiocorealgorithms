from ..general.decorators import job_header, process_header, store_job_result
from defs import SCRIPT_CASCADE_FACE_DETECTOR, create_cascade_detector
from ...algorithms.cascades.script_cascade_detector import ScriptTask
from ..general.process_interface import AlgorithmProcessInterface
from ...algorithms.cascades.tools import getROIImage
from ...algorithm_storage import AlgorithmStorage
from ..general.handling import parse_database
from ...flows import ResizeImageAlgorithm
import ast
import cv2
import os


def job(callback_code, **kwargs):
    process = CascadeDetectionApplyProcess(None)
    CascadeDetectionApplyProcess.job(callback_code, **kwargs)


class CascadeDetectionApplyProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        if not AlgorithmStorage.instance().exists(SCRIPT_CASCADE_FACE_DETECTOR):
            AlgorithmStorage.instance().register(SCRIPT_CASCADE_FACE_DETECTOR, create_cascade_detector())

    @classmethod
    @store_job_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        record = CascadeDetectionApplyProcess.process(**kwargs)
        return CascadeDetectionApplyProcess.create_result_message(record)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        data_list = kwargs['data_list']
        tasks = {}
        record = {}
        for data_str in data_list:
            data_obj = ast.literal_eval(data_str)
            task_obj = ScriptTask.parse(data_obj['task'])
            tasks[task_obj.name] = parse_database(data_obj['task_result'])
            data_copy = data_obj.copy()
            del data_copy['task']
            del data_copy['task_result']
            record.update(data_copy)
        img = cv2.imread(record['data'])
        detector = AlgorithmStorage.instance().get(SCRIPT_CASCADE_FACE_DETECTOR)
        res = detector.detect(img, tasks)
        roi_path = os.path.join(record['temp_image_path'], "face_det_roi.png")
        roi_img = getROIImage(img, res[1][0])
        resizer = ResizeImageAlgorithm({})
        cv2.imwrite(roi_path, resizer.apply({'img': roi_img})['img'])
        record['roi'] = roi_path
        return record

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
