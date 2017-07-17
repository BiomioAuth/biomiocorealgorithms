from cascade_detect_prepare_process import CascadeDetectionPrepareProcess
from cascade_detect_init_process import CascadeDetectionInitialProcess
from cascade_detect_apply_process import CascadeDetectionApplyProcess
from ..general.process_interface import AlgorithmProcessInterface


class CascadeDetectionProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        detect_init_process = CascadeDetectionInitialProcess(worker)
        detect_prepare_process = CascadeDetectionPrepareProcess(worker)
        detect_apply_process = CascadeDetectionApplyProcess(worker)
        detect_init_process.set_next_process(detect_prepare_process)
        detect_prepare_process.set_next_process(detect_apply_process)
        self._start_process = detect_init_process
        self._end_process = detect_apply_process

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._end_process.set_next_process(self._next_process)
        self._start_process.run(worker, kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer,
                                **kwargs)
