from ...algorithms.cascades.tools import skipEmptyRectangles, isRectangle, loadScript
from ..general.decorators import job_header, process_header, store_partial_result
from ...algorithms.cascades.scripts_detectors import RotatedCascadesDetector
from ..general.process_interface import AlgorithmProcessInterface
from ...algorithms.cvtools import numpy_ndarrayToList, rotate90
from ..general.handling import load_temp_data, save_temp_data
from ...algorithms.cascades import SCRIPTS_PATH
from settings.settings import get_settings
import os


def job(callback_code, **kwargs):
    RotationDetectionProcess.job(callback_code, **kwargs)


class RotationDetectionProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)

    @classmethod
    @store_partial_result
    @job_header
    def job(cls, callback_code, **kwargs):
        """
        Job function for rotation detecting.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'data_file': data file path,
                'angle': angle key value
            }
        """
        return {'data_file': RotationDetectionProcess.process(**kwargs)}

    @classmethod
    @process_header
    def process(cls, **kwargs):
        source = load_temp_data(kwargs['data_file'], remove=False)
        settings = get_settings(source['algoID'])
        img = source['data']
        for i in range(0, kwargs["angle"], 1):
            img = rotate90(img)
        rects = []
        d = dict()
        rotation_script_dict = loadScript(os.path.join(SCRIPTS_PATH, settings['rotation_script']))
        rotation_script = RotatedCascadesDetector.init_stage(rotation_script_dict)
        detector = RotatedCascadesDetector(rotation_script_dict, dict())
        if len(rotation_script.stages) > 1:
            r = []
            for stage in rotation_script.stages:
                lr1 = detector.apply_stage(img, stage)
                r += lr1
                for lr in lr1:
                    d[str(lr)] = kwargs["angle"] + 1
            if isRectangle(r[0]):
                rects = skipEmptyRectangles(r)
        else:
            stage = rotation_script.stages[0]
            r1 = detector.apply_stage(img, stage)
            rects += r1
            for lr in r1:
                d[str(lr)] = kwargs["angle"] + 1
            rects = skipEmptyRectangles(rects)
        source.update({'data': img, 'data_angle': kwargs["angle"] + 1,
                       'roi_rects': [numpy_ndarrayToList(r) for r in rects], 'datagram': d})
        training_process_data = save_temp_data(source, source['temp_data_path'], ['data'])
        return training_process_data

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        # kwargs.update({'timeout': 300})
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
