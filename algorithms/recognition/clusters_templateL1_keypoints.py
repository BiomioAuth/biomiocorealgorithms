from __future__ import absolute_import
import logger
from biomio.algorithms.algorithms.features.matchers import Matcher, BruteForceMatcherType
from biomio.algorithms.algorithms.recognition.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.algorithms.recognition.keypoints import (listToNumpy_ndarray, numpy_ndarrayToList,
                                                                verifying)
import numpy


class ClustersTemplateL1MatchingDetector(ClustersMatchingDetector):
    def __init__(self):
        ClustersMatchingDetector.__init__(self)

    def update_hash(self, data):
        del data['keypoints']
        del data['descriptors']
        self._hash.append(data)
        self.update_hash_templateL1(data)

    def update_hash_templateL1(self, data):
        """

        max_weight = se*suma(i=1,k-1: 1+2*i) + k*(n-k)*se,
        where
            n - count of images,
            k - count of identical matches, k <= n,
            se - single estimate, I used se=1

        :param data:
        :return:
        """
        if len(self._hash) == 1:
            self._etalon = []
            for cluster in data['clusters']:
                weight_cluster = []
                if cluster is not None:
                    weight_cluster = [(desc, 1) for desc in cluster]
                self._etalon.append(weight_cluster)
        else:
            matcher = Matcher(BruteForceMatcherType)
            for index in range(0, len(self._etalon)):
                dt_cluster = data['clusters'][index]
                if dt_cluster is None or len(dt_cluster) == 0:
                    continue
                et_cluster = self._etalon[index]
                for obj in self._hash:
                    if data['path'] == obj['path']:
                        continue
                    ob_cluster = obj['clusters'][index]
                    if ob_cluster is None or len(ob_cluster) == 0:
                        continue
                    matches1 = matcher.knnMatch(listToNumpy_ndarray(ob_cluster),
                                                listToNumpy_ndarray(dt_cluster), k=5)
                    for v in matches1:
                        if len(v) >= 1:
                            best = None
                            dist = -1
                            for m in v:
                                if m.distance == 0:
                                    best = m
                                    dist = 0
                                else:
                                    for d, c in et_cluster:
                                        if dist < c / (1.0 * m.distance):
                                            dist = c / (1.0 * m.distance)
                                            best = m
                                        break
                            ob_is = False
                            dt_is = False
                            new_cluster = []
                            for d, c in et_cluster:
                                if numpy.array_equal(d, ob_cluster[best.queryIdx]):
                                    c += 1
                                    ob_is = True
                                if numpy.array_equal(d, dt_cluster[best.trainIdx]):
                                    c += 1
                                    dt_is = True
                                new_cluster.append((d, c))
                            if not ob_is:
                                new_cluster.append((ob_cluster[best.queryIdx], 1))
                            if not dt_is:
                                new_cluster.append((dt_cluster[best.trainIdx], 1))
                            et_cluster = new_cluster
                    self._etalon[index] = et_cluster

    def importSources(self, source):
        logger.algo_logger.debug("Database loading started...")
        self.importSources_L1Template(source.get('data', dict()))
        self._prob = source.get('threshold', 100)
        logger.algo_logger.debug("Database loading finished.")

    def importSources_L1Template(self, source):
        self._etalon = [[] for key in source.keys()]
        for c_num, cluster in source.iteritems():
            etalon_cluster = [[] for key in cluster.keys()]
            for d_num, desc_dict in cluster.iteritems():
                etalon_cluster[int(d_num)] = (listToNumpy_ndarray(desc_dict['descriptor']),
                                              int(desc_dict['count']))
            self._etalon[int(c_num)] = etalon_cluster

    def exportSources(self):
        data = self.exportSources_L1Template()
        source = dict()
        if len(data.keys()) > 0:
            source = dict()
            source['data'] = data
            source['threshold'] = self._prob
        return source

    def exportSources_L1Template(self):
        sources = dict()
        for index in range(0, len(self._etalon)):
            et_weight_cluster = self._etalon[index]
            cluster = dict()
            i = 0
            for d, c in et_weight_cluster:
                obj = dict()
                obj['descriptor'] = numpy_ndarrayToList(d)
                obj['count'] = c
                cluster[str(i)] = obj
                i += 1
            sources[str(index)] = cluster
        return sources

    @verifying
    def verify(self, data):
        return self.verify_template_L1(data)

    def verify_template_L1(self, data):
        matcher = Matcher(BruteForceMatcherType)
        res = []
        prob = 0
        logger.algo_logger.debug("Image: " + data['path'])
        logger.algo_logger.debug("Template size: ")
        for index in range(0, len(self._etalon)):
            et_weight_cluster = self._etalon[index]
            et_cluster = []
            cluster_weight = 0
            for d, c in et_weight_cluster:
                if c > 0:
                    et_cluster.append(d)
                    cluster_weight += c
            dt_cluster = data['clusters'][index]
            ms = []
            if et_cluster is None or dt_cluster is None:
                continue
            if len(et_cluster) > 0 and len(dt_cluster) > 0:
                matches1 = matcher.knnMatch(listToNumpy_ndarray(et_cluster, numpy.uint8),
                                            listToNumpy_ndarray(dt_cluster, numpy.uint8), k=2)
                matches2 = matcher.knnMatch(listToNumpy_ndarray(dt_cluster, numpy.uint8),
                                            listToNumpy_ndarray(et_cluster, numpy.uint8), k=2)
                for v in matches1:
                    if len(v) >= 1:
                        for m in v:
                            for c in matches2:
                                if len(c) >= 1:
                                    for n in c:
                                        if m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx:
                                            ms.append(et_cluster[m.queryIdx])
                # TODO: I think, next part can be rewritten using filter() and chain() functions
                c_val = 0
                for item in ms:
                    for d, c in et_weight_cluster:
                        if numpy.array_equal(d, item):
                            c_val += c
                #
                res.append(c_val / cluster_weight)
                val = (c_val / (1.0 * cluster_weight)) * 100
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(cluster_weight)
                                         + " Positive: " + str(c_val) + " Probability: " + str(val))
                prob += val
            else:
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(cluster_weight)
                                         + " Invalid.")
        logger.algo_logger.debug("Probability: " + str((prob / (1.0 * len(res)))))
        return prob / (1.0 * len(res))
