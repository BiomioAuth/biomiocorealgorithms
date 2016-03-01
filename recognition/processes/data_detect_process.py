from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from defs import (STATUS_RESULT, STATUS_ERROR, UNKNOWN_ERROR, REDIS_GENERAL_DATA, REDIS_CLUSTER_JOB_ACTION,
                  JOB_STATUS_ACTIVE, JOB_STATUS_FINISHED, INTERNAL_TRAINING_ERROR, ERROR_FORMAT, REDIS_TEMPLATE_RESULT)
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.cascades.scripts_detectors import CascadesDetectionInterface
from biomio.algorithms.recognition.processes.settings.settings import get_settings
from biomio.algorithms.recognition.kodsettings import KODSettings
from messages import create_error_message, create_result_message
from biomio.algorithms.features.features import FeatureDetector
from biomio.algorithms.cvtools.types import numpy_ndarrayToList
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from biomio.algorithms.features import constructDetector
from biomio.algorithms.cascades.tools import loadScript
from biomio.algorithms.clustering import KMeans, FOREL
from handling import load_temp_data, save_temp_data
from settings import loadSettings
import ast


DATA_DETECTION_PROCESS_CLASS_NAME = "DataDetectionProcess"

def job(callback_code, **kwargs):
    DataDetectionProcess.job(callback_code, **kwargs)


class DataDetectionProcess(AlgorithmProcessInterface):
    def __init__(self, temp_data_path, worker):
        AlgorithmProcessInterface.__init__(self, temp_data_path, worker)
        self._classname = DATA_DETECTION_PROCESS_CLASS_NAME
        self._cluster_match_process = None
        self._final_process = AlgorithmProcessInterface()

    def set_cluster_matching_process(self, process):
        self._cluster_match_process = process

    def set_final_training_process(self, process):
        self._final_process = process

    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary:
            {
                'status': 'result',
                'data':
                    [
                        {
                            'data_file': data file path
                        }
                    ],
                'type': 'matching'
            }
        """
        self._handler_logger_info(result)
        if self._cluster_match_process is not None:
            self._matching_handler(result)
        elif self._final_process is not None:
            self._final_process.run(self._worker, **result['data'][0])
        else:
            logger.debug("Handler not found!!!")

    def _matching_handler(self, result):
        if result is not None:
            if result['status'] == STATUS_ERROR:
                general_key = REDIS_GENERAL_DATA % result['details']['userID']
                data = dict()
                fault = 0
                if AlgorithmsDataStore.instance().exists(general_key):
                    data = ast.literal_eval(AlgorithmsDataStore.instance().get_data(general_key))
                    AlgorithmsDataStore.instance().delete_data(general_key)
                    fault = data.get('image_fault', 0)
                data['image_fault'] = fault + 1
                AlgorithmsDataStore.instance().store_data(general_key, **data)
                logger.debug("IMAGE FAULT")
                logger.debug(data['image_fault'])
            elif result['status'] == STATUS_RESULT:
                logger.debug(result['data'][0]['data_file'])
                res_data = load_temp_data(result['data'][0]['data_file'], remove=True)
                logger.debug(res_data["name"])
                for key, cluster in res_data['clusters'].iteritems():
                    current_key = REDIS_CLUSTER_JOB_ACTION % key
                    logger.debug(current_key)
                    if AlgorithmsDataStore.instance().exists(current_key):
                        data = AlgorithmsDataStore.instance().get_data(current_key)
                        AlgorithmsDataStore.instance().delete_data(current_key)
                        logger.debug("@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$@")
                        logger.debug(data['status'])
                        if data['status'] == JOB_STATUS_ACTIVE:
                            if cluster is not None and len(cluster) > 0:
                                queue = data.get('queued_data', [])
                                queue.append(cluster)
                                data['queued_data'] = queue
                            else:
                                step = data['step']
                                data['step'] = step + 1
                            AlgorithmsDataStore.instance().store_data(current_key, **data)
                        elif data['status'] == JOB_STATUS_FINISHED:
                            step = data['step']
                            data['step'] = step + 1
                            logger.debug("TEST#---#CLUSTERS")
                            logger.debug(current_key)
                            logger.debug(data['step'])
                            if cluster is not None and len(cluster) > 0:
                                data['status'] = JOB_STATUS_ACTIVE
                                AlgorithmsDataStore.instance().store_data(current_key, **data)
                                job_data = {
                                    'cluster': cluster,
                                    'template': data['template'],
                                    'userID': data['userID'],
                                    'algoID': data['algoID'],
                                    'cluster_id': key
                                }
                                if 'providerID' in data:
                                    job_data.update({'providerID': data['providerID']})
                                self._cluster_match_process.run(self._worker, **job_data)
                            else:
                                fault = 0
                                general_key = REDIS_GENERAL_DATA % data['userID']
                                if AlgorithmsDataStore.instance().exists(general_key):
                                    general_data = AlgorithmsDataStore.instance().get_data(general_key)
                                    fault = general_data['image_fault']
                                logger.debug(fault)
                                if data['step'] == 5 - fault:
                                    template_key = REDIS_TEMPLATE_RESULT % data['userID']
                                    final_data = dict()
                                    ended = 0
                                    if AlgorithmsDataStore.instance().exists(template_key):
                                        final_data = ast.literal_eval(
                                            AlgorithmsDataStore.instance().get_data(template_key))
                                        AlgorithmsDataStore.instance().delete_data(template_key)
                                        ended = final_data['ended']
                                    else:
                                        final_data['userID'] = data['userID']
                                        final_data['algoID'] = data['algoID']
                                        if 'providerID' in data:
                                            final_data['providerID'] = data['providerID']
                                        final_data['temp_data_path'] = data['temp_data_path']
                                        final_data['general_data'] = data['general_data']
                                    if final_data.get(str(key), None) is None:
                                        final_data['ended'] = ended + 1
                                        final_data[str(key)] = data['template']
                                        key_list = final_data.get('clusters_list', [])
                                        key_list.append(str(key))
                                        final_data['clusters_list'] = key_list
                                        if final_data['ended'] == 6:
                                            self._final_process.run(self._worker, **final_data)
                                        else:
                                            AlgorithmsDataStore.instance().store_data(template_key, **final_data)
                                else:
                                    AlgorithmsDataStore.instance().store_data(current_key, **data)
                        else:
                            logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, UNKNOWN_ERROR))
                    else:
                        data = {
                            'template': cluster,
                            'status': JOB_STATUS_FINISHED,
                            'userID': res_data['userID'],
                            'algoID': res_data['algoID'],
                            'temp_data_path': res_data['temp_data_path'],
                            'general_data': res_data['general_data'],
                            'step': 1
                        }
                        if 'providerID' in res_data:
                            data.update({'providerID': res_data['providerID']})
                        AlgorithmsDataStore.instance().store_data(key=current_key, **data)

    @staticmethod
    def job(callback_code, **kwargs):
        """
        Job function for data detection (Feature Detection, Feature Clustering and Feature Extraction).

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'data_file': data file path
            }
        """
        kwargs.update({'callback_code': callback_code})
        DataDetectionProcess._job_logger_info(DATA_DETECTION_PROCESS_CLASS_NAME, **kwargs)
        record = DataDetectionProcess.process(**kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        DataDetectionProcess._process_logger_info(DATA_DETECTION_PROCESS_CLASS_NAME, **kwargs)
        source = load_temp_data(kwargs['data_file'], remove=True)
        temp_data_path = source['temp_data_path']
        settings = get_settings(source['algoID'])
        logger.debug(settings)
        logger.debug(loadSettings(settings['kodsettings']))
        kodsettings = KODSettings()
        kodsettings.importSettings(loadSettings(settings['kodsettings'])['KODSettings'])
        logger.debug("DEBUG::DataDetectionProcess::%s::FeatureDetector::create" % str(kwargs['callback_code']))
        detector = FeatureDetector(constructDetector(kodsettings.detector_type, kodsettings.settings))

        try:
            logger.debug("DEBUG::DataDetectionProcess::%s::FeatureDetector::detect" % str(kwargs['callback_code']))
            obj = detector.detectAndCompute(source['roi'])
            logger.debug("DEBUG::DataDetectionProcess::%s::FeatureDetector::store" % str(kwargs['callback_code']))
            source['keypoints'] = obj['keypoints']
            source['descriptors'] = obj['descriptors']
            if source['descriptors'] is None:
                source['descriptors'] = []
            logger.debug("DEBUG::DataDetectionProcess::%s::Clustering" % str(kwargs['callback_code']))
            record = DataDetectionProcess._detect_process(source, detector, temp_data_path, kwargs['callback_code'])
        except Exception as err:
            logger.debug(err.message)
            record = create_error_message(INTERNAL_TRAINING_ERROR, 'data', err.message)
        return record

    @staticmethod
    def _detect_process(data, detector, path, callback_code):
        logger.debug("DEBUG::DataDetectionProcess::%s::EyesDetection" % str(callback_code))
        eyeROI = CascadesDetectionInterface(loadScript("main_haarcascade_eyes_union.json", True))
        rect = eyeROI.detect(data['roi'])[1]
        if len(rect) <= 0 or len(rect[0]) <= 0:
            logger.info("Eye ROI wasn't found.")
            return create_error_message(INTERNAL_TRAINING_ERROR, "data", "Eye ROI wasn't found.", data['userID'])
        rect = rect[0]
        logger.debug("DEBUG::DataDetectionProcess::%s::ClusterInitCenters" % str(callback_code))
        lefteye = (rect[0] + rect[3], rect[1] + rect[3] / 2)
        righteye = (rect[0] + rect[2] - rect[3], rect[1] + rect[3] / 2)
        centereye = (lefteye[0] + (righteye[0] - lefteye[0]) / 2, lefteye[1] + (righteye[1] - lefteye[1]) / 2)
        centernose = (lefteye[0] + (righteye[0] - lefteye[0]) / 2, rect[1] + 2 * rect[3])
        centermouth = (centernose[0], centernose[1] + rect[3])
        leftmouth = (lefteye[0], centermouth[1])
        rightmouth = (righteye[0], centermouth[1])
        centers = [lefteye, righteye, centereye, centernose, leftmouth, rightmouth]
        # DataDetectionProcess._filter_keypoints(data)

        logger.debug("DEBUG::DataDetectionProcess::%s::KMeans" % str(callback_code))
        clusters = KMeans(data['keypoints'], 0, centers)
        logger.debug("DEBUG::DataDetectionProcess::%s::CheckClusters" % str(callback_code))
        data['true_clusters'] = clusters
        descriptors = dict()
        active_clusters = 0
        for index, cluster in enumerate(clusters):
            desc = detector.compute(data['roi'], cluster['items'])
            curr_cluster = desc['descriptors']
            descriptors[str(index)] = numpy_ndarrayToList(curr_cluster) if curr_cluster is not None else []
            if curr_cluster is not None and len(curr_cluster) > 0:
                active_clusters += 1
        data['clusters'] = descriptors
        if active_clusters < len(centers) - 2:
            logger.info("Number of clusters are insufficient for the recognition.")
            return create_error_message(INTERNAL_TRAINING_ERROR, "clusters",
                                        "Number of clusters are insufficient for the recognition.", data['userID'])
        logger.debug("DEBUG::DataDetectionProcess::%s::RemoveUnused" % str(callback_code))
        data.pop("keypoints", None)
        data.pop("true_clusters", None)
        logger.debug("DEBUG::DataDetectionProcess::%s::SaveResults" % str(callback_code))
        data["descriptors"] = numpy_ndarrayToList(data["descriptors"])
        matching_process_data = save_temp_data(data, path, ['data', 'roi'])
        logger.debug("DEBUG::DataDetectionProcess::%s::ReturnResult" % str(callback_code))
        return create_result_message([{'data_file': matching_process_data}], 'matching')

    @staticmethod
    def _filter_keypoints(data):
        clusters = FOREL(data['keypoints'], 20)
        keypoints = []
        for cluster in clusters:
            p = len(cluster['items']) / (1.0 * len(data['keypoints']))
            if p > 0.02:
                keypoints += [item for item in cluster['items']]
        data['keypoints'] = keypoints

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
