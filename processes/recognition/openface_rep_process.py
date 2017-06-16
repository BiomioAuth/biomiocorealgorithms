from ..general.decorators import job_header, process_header, store_job_result
from ..general.process_interface import AlgorithmProcessInterface
from ... import OPENFACE_IMAGE_DIMENSION, OPENFACE_NN4_MODEL_PATH
from ...flows import OpenFaceDataRepresentation
import os


def job(callback_code, **kwargs):
    OpenFaceRepresentationProcess.job(callback_code, **kwargs)


class OpenFaceRepresentationProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)

    @classmethod
    @job_header
    @store_job_result
    def job(cls, callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary
        """
        record = OpenFaceRepresentationProcess.process(**kwargs)
        return OpenFaceRepresentationProcess.create_result_message(record)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        if kwargs is None:
            # TODO: Write Error handler
            return kwargs
        result = kwargs.copy()
        openface_representation = OpenFaceDataRepresentation({
            'networkModel': OPENFACE_NN4_MODEL_PATH,
            'imgDim': OPENFACE_IMAGE_DIMENSION#,
            # 'error_handler': error_handler
        })

        path = kwargs.get('data')
        if kwargs.get('backup_image_path', None) is not None:
            path = os.path.join(kwargs.get('backup_image_path'), os.path.basename(path))
        tdata = openface_representation.apply({'path': path, 'options': kwargs.get('options', {})})
        result.update({'rep': tdata})
        openface_representation.clean()
        return result

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
