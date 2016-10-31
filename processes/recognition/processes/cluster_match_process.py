from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore, REDIS_DO_NOT_STORE_RESULT_KEY
from defs import (JOB_STATUS_ACTIVE, JOB_STATUS_FINISHED, STATUS_ERROR, STATUS_RESULT,
                  REDIS_CLUSTER_JOB_ACTION, REDIS_GENERAL_DATA, REDIS_TEMPLATE_RESULT,
                  ERROR_FORMAT, INTERNAL_TRAINING_ERROR, UNKNOWN_ERROR)
from ....algorithms.features import matcherForDetector, dtypeForDetector
from ....algorithms.cvtools.types import listToNumpy_ndarray
from ....interfaces import AlgorithmProcessInterface, logger
from ....algorithms.features.matchers import Matcher
from settings.settings import get_settings
from messages import create_result_message
from ..kodsettings import KODSettings
from settings import loadSettings
import itertools
import ast


CLUSTER_MATCHING_PROCESS_CLASS_NAME = "ClusterMatchingProcess"

def job(callback_code, **kwargs):
    ClusterMatchingProcess.job(callback_code, **kwargs)


class ClusterMatchingProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, "", worker)
        self._classname = CLUSTER_MATCHING_PROCESS_CLASS_NAME
        self._cluster_match_process = self
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
                {
                    'userID': user identifier string,
                    'algoID': algorithm identifier string,
                    'template': descriptor list,
                    'cluster_id': cluster identifier,
                    'cluster': descriptor list
                },
                'type': 'matching'
            }
        """
        self._handler_logger_info(result)
        if result is not None:
            if result['status'] == STATUS_ERROR:
                logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, UNKNOWN_ERROR))
            elif result['status'] == STATUS_RESULT:
                res_data = result['data']
                cluster_id = res_data['cluster_id']
                current_key = REDIS_CLUSTER_JOB_ACTION % cluster_id
                if AlgorithmsDataStore.instance().exists(current_key):
                    data = AlgorithmsDataStore.instance().get_data(current_key)
                    # data = ast.literal_eval(AlgorithmsDataStore.instance().get_data(current_key))
                    AlgorithmsDataStore.instance().delete_data(current_key)
                    if data['status'] == JOB_STATUS_ACTIVE:
                        data['template'] = res_data['template']
                        queued = data.get('queued_data', None)
                        if queued is None or len(queued) <= 0:
                            data['status'] = JOB_STATUS_FINISHED
                            logger.debug("TEST##CLUSTERS")
                            logger.debug(current_key)
                            logger.debug(data['step'])
                            logger.debug("IMAGE FAULT")
                            general_key = REDIS_GENERAL_DATA % data['userID']
                            fault = 0
                            if AlgorithmsDataStore.instance().exists(general_key):
                                general_data = AlgorithmsDataStore.instance().get_data(general_key)
                                # general_data = ast.literal_eval(AlgorithmsDataStore.instance().get_data(general_key))
                                fault = general_data['image_fault']
                            logger.debug(fault)
                            if data['step'] == 5 - fault:
                                template_key = REDIS_TEMPLATE_RESULT % data['userID']
                                final_data = dict()
                                ended = 0
                                if AlgorithmsDataStore.instance().exists(template_key):
                                    final_data = AlgorithmsDataStore.instance().get_data(template_key)
                                    # final_data = ast.literal_eval(
                                    #     AlgorithmsDataStore.instance().get_data(template_key))
                                    AlgorithmsDataStore.instance().delete_data(template_key)
                                    ended = final_data['ended']
                                else:
                                    final_data['userID'] = data['userID']
                                    final_data['algoID'] = data['algoID']
                                    if 'providerID' in data:
                                        final_data['providerID'] = data['providerID']
                                    final_data['temp_data_path'] = data['temp_data_path']
                                    final_data['general_data'] = data['general_data']
                                if final_data.get(str(cluster_id), None) is None:
                                    final_data['ended'] = ended + 1
                                    final_data[str(cluster_id)] = data['template']
                                    key_list = final_data.get('clusters_list', [])
                                    key_list.append(str(cluster_id))
                                    final_data['clusters_list'] = key_list
                                    if final_data['ended'] == 6:
                                        self._final_process.run(self._worker, **final_data)
                                    else:
                                        AlgorithmsDataStore.instance().store_data(template_key, **final_data)
                            else:
                                AlgorithmsDataStore.instance().store_data(current_key, **data)
                        else:
                            cluster = queued.pop(0)
                            data['queued_data'] = queued
                            step = data['step']
                            data['step'] = step + 1
                            job_data = {
                                'cluster': cluster,
                                'template': data['template'],
                                'userID': data['userID'],
                                'algoID': data['algoID'],
                                'cluster_id': cluster_id
                            }
                            if 'providerID' in data:
                                job_data.update({'providerID': data['providerID']})
                            AlgorithmsDataStore.instance().store_data(current_key, **data)
                            self._cluster_match_process.run(self._worker, **job_data)
                    else:
                        logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, UNKNOWN_ERROR))
                else:
                    logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, UNKNOWN_ERROR))

    @staticmethod
    def job(callback_code, **kwargs):
        """
        Job function for cluster matching of template cluster and data cluster.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'cluster_id': cluster identifier,
                'userID': user identifier string,
                'template': descriptor list,
                'algoID': algorithm identifier string,
                'cluster': descriptor list
            }
        """
        ClusterMatchingProcess._job_logger_info(CLUSTER_MATCHING_PROCESS_CLASS_NAME, **kwargs)
        data = ClusterMatchingProcess.process(**kwargs)
        record = create_result_message(data, 'matching')
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        ClusterMatchingProcess._process_logger_info(CLUSTER_MATCHING_PROCESS_CLASS_NAME, **kwargs)
        data = kwargs.copy()
        settings = get_settings(data['algoID'])
        logger.debug(settings)
        kodsettings = KODSettings()
        kodsettings.importSettings(loadSettings(settings['kodsettings'])['KODSettings'])
        logger.debug(kodsettings)
        matcher = Matcher(matcherForDetector(kodsettings.detector_type))
        et_cluster = data['template']
        dt_cluster = data['cluster']
        if ((et_cluster is not None and len(et_cluster) > settings['knn']) and
                (dt_cluster is not None and len(dt_cluster) > settings['knn'])):
            dtype = dtypeForDetector(kodsettings.detector_type)
            matches1 = matcher.knnMatch(listToNumpy_ndarray(et_cluster, dtype),
                                        listToNumpy_ndarray(dt_cluster, dtype), k=settings['knn'])
            matches2 = matcher.knnMatch(listToNumpy_ndarray(dt_cluster, dtype),
                                        listToNumpy_ndarray(et_cluster, dtype), k=settings['knn'])
            good = list(itertools.chain.from_iterable(itertools.imap(
                lambda(x, _): (et_cluster[x.queryIdx], dt_cluster[x.trainIdx]), itertools.ifilter(
                    lambda(m, n): m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx, itertools.product(
                        itertools.chain(*matches1), itertools.chain(*matches2)
                    )
                )
            )))
            et_cluster = good
        data['template'] = et_cluster
        return data

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
