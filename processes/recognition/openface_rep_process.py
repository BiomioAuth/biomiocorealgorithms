from ..general.decorators import job_header, process_header, store_job_result
from ..general.process_interface import AlgorithmProcessInterface
from ... import OPENFACE_IMAGE_DIMENSION, OPENFACE_NN4_MODEL_PATH
from ...algorithm_storage import AlgorithmStorage
from ..general.handling import serialize_database
from ...flows import OpenFaceDataRepresentation
from defs import OPENFACE_REPRESENTATION
import os


def job(callback_code, **kwargs):
    process = OpenFaceRepresentationProcess(None)
    OpenFaceRepresentationProcess.job(callback_code, **kwargs)


class OpenFaceRepresentationProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        if not AlgorithmStorage.instance().exists(OPENFACE_REPRESENTATION):
            AlgorithmStorage.instance().register(OPENFACE_REPRESENTATION, OpenFaceDataRepresentation({
            'networkModel': OPENFACE_NN4_MODEL_PATH,
            'imgDim': OPENFACE_IMAGE_DIMENSION#,
            # 'error_handler': error_handler
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
        record = OpenFaceRepresentationProcess.process(**kwargs)
        return OpenFaceRepresentationProcess.create_result_message(record)

    @classmethod
    @process_header
    def process(cls, **kwargs):
        if kwargs is None:
            # TODO: Write Error handler
            return kwargs
        result = kwargs.copy()
        openface_representation = AlgorithmStorage.instance().get(OPENFACE_REPRESENTATION)

        path = kwargs.get('data')
        if kwargs.get('roi') is None:
            if kwargs.get('backup_image_path', None) is not None:
                path = os.path.join(kwargs.get('backup_image_path'), os.path.basename(path))
        else:
            path = kwargs.get('roi')
        tdata = openface_representation.apply({'path': path, 'options': kwargs.get('options', {})})
        result.update({'rep': serialize_database(tdata['rep'])})
        openface_representation.clean()
        return result

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
