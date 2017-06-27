from ...flows import DLibFaceDetectionAlgorithm, INNER_EYES_AND_BOTTOM_LIP, DLIB_PREDICTOR_V2
from ..general.decorators import job_header, process_header, store_job_result
from ..general.process_interface import AlgorithmProcessInterface
from ... import DLIB_MODEL_PATH, OPENFACE_IMAGE_DIMENSION
from ...algorithm_storage import AlgorithmStorage
from defs import DLIB_FACE_DETECTOR
import cv2
import os


def job(callback_code, **kwargs):
    process = DLibFaceDetectionProcess(None)
    DLibFaceDetectionProcess.job(callback_code, **kwargs)


class DLibFaceDetectionProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        if not AlgorithmStorage.instance().exists(DLIB_FACE_DETECTOR):
            AlgorithmStorage.instance().register(DLIB_FACE_DETECTOR, DLibFaceDetectionAlgorithm({
                'dlibFacePredictor': DLIB_MODEL_PATH,
                'landmarkIndices': INNER_EYES_AND_BOTTOM_LIP,
                'predictorVersion': DLIB_PREDICTOR_V2,
                'imgDim': OPENFACE_IMAGE_DIMENSION
            }))

    @classmethod
    @store_job_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        return DLibFaceDetectionProcess.create_result_message(DLibFaceDetectionProcess.process(**kwargs))

    @classmethod
    @process_header
    def process(cls, **kwargs):
        img = cv2.imread(kwargs['data'])
        detector = AlgorithmStorage.instance().get(DLIB_FACE_DETECTOR)
        res = detector.apply({'img': img, 'path': kwargs['data']})
        record = kwargs.copy()
        if res['img'] is not None:
            roi_path = os.path.join(kwargs['temp_image_path'], "face_det_roi.png")
            cv2.imwrite(roi_path, res['img'])
            record.update({'roi': roi_path})
        else:
            record.update({'roi': None})
        return record

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
