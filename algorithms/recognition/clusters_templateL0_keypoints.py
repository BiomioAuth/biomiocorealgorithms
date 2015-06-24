from __future__ import absolute_import
import logger
from biomio.algorithms.algorithms.features.matchers import Matcher, BruteForceMatcherType
from biomio.algorithms.algorithms.recognition.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.algorithms.cvtools.types import listToNumpy_ndarray, numpy_ndarrayToList
from biomio.algorithms.algorithms.recognition.keypoints import verifying
import itertools
import numpy
import sys


class ClustersTemplateL0MatchingDetector(ClustersMatchingDetector):
    def __init__(self):
        ClustersMatchingDetector.__init__(self)

    def threshold(self):
        return self._coff * self._prob

    def update_hash(self, data):
        del data['keypoints']
        del data['descriptors']
        self._hash.append(data)
        self.update_hash_templateL0(data)

    def update_hash_templateL0(self, data):
        if len(self._etalon) == 0:
            self._etalon = data['clusters']
        else:
            matcher = Matcher(BruteForceMatcherType)
            for index in range(0, len(self._etalon)):
                et_cluster = self._etalon[index]
                dt_cluster = data['clusters'][index]
                if et_cluster is None or len(et_cluster) == 0:
                    self._etalon[index] = et_cluster
                elif dt_cluster is None or len(dt_cluster) == 0:
                    self._etalon[index] = et_cluster
                else:
                    matches1 = matcher.knnMatch(et_cluster, dt_cluster, k=3)
                    matches2 = matcher.knnMatch(dt_cluster, et_cluster, k=3)
                    good = []
                    for v in matches1:
                        if len(v) >= 1:
                            for m in v:
                                for c in matches2:
                                    if len(c) >= 1:
                                        for n in c:
                                            if m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx:
                                                good.append(et_cluster[m.queryIdx])
                                                good.append(dt_cluster[m.trainIdx])
                    self._etalon[index] = listToNumpy_ndarray(good)

    def update_database(self):
        try:
            self._prob = min(self._hash, key=self.verify_template_L0)
        except:
            self._prob = sys.maxint

    def importSources(self, source):
        logger.algo_logger.debug("Database loading started...")
        self.importSources_L0Template(source.get('data', dict()))
        self._prob = source.get('threshold', 100)
        logger.algo_logger.debug("Database loading finished.")

    def importSources_L0Template(self, source):
        self._etalon = [[] for key in source.keys()]
        for c_num, cluster in source.iteritems():
            etalon_cluster = [listToNumpy_ndarray(descriptor) for d_num, descriptor in cluster.iteritems()]
            self._etalon[int(c_num)] = etalon_cluster

    def exportSources(self):
        data = self.exportSources_L0Template()
        source = dict()
        if len(data.keys()) > 0:
            source = dict()
            source['data'] = data
            source['threshold'] = self._prob
        return source

    def exportSources_L0Template(self):
        sources = dict()
        for index in range(0, len(self._etalon)):
            cluster = self._etalon[index]
            cluster_dict = dict()
            i_desc = 0
            if cluster is None:
                cluster = []
            for descriptor in cluster:
                cluster_dict[i_desc] = numpy_ndarrayToList(descriptor)
                i_desc += 1
            sources[str(index)] = cluster_dict
        return sources

    @verifying
    def verify(self, data):
        return self.verify_template_L0(data)

    def verify_template_L0(self, data):
        matcher = Matcher(BruteForceMatcherType)
        res = []
        prob = 0
        logger.algo_logger.debug("Image: " + data['path'])
        logger.algo_logger.debug("Template size: ")
        # TODO: I modified next for, but maybe we can modify it more.
        summ = 0
        for et_cluster in self._etalon:
            if et_cluster is not None:
                summ += len(et_cluster)
        for index in range(0, len(self._etalon)):
            et_cluster = self._etalon[index]
            dt_cluster = data['clusters'][index]
            ms = []
            if et_cluster is None:
                res.append(ms)
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(-1)
                                         + " Invalid. (Weight: 0)")
                continue
            if dt_cluster is None:
                res.append(ms)
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(len(self._etalon[index]))
                                         + " Positive: 0 Probability: 0 (Weight: " +
                                         str(len(et_cluster) / (1.0 * summ)) + ")")
                continue
            if len(et_cluster) > 0 and len(dt_cluster) > 0:
                matches1 = matcher.knnMatch(listToNumpy_ndarray(et_cluster, numpy.uint8),
                                            listToNumpy_ndarray(dt_cluster, numpy.uint8), k=2)
                matches2 = matcher.knnMatch(listToNumpy_ndarray(dt_cluster, numpy.uint8),
                                            listToNumpy_ndarray(et_cluster, numpy.uint8), k=2)
                ms = map(
                    lambda(x, _): x, itertools.ifilter(
                        lambda(m, n): m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx, itertools.product(
                            itertools.chain(*matches1), itertools.chain(*matches2)
                        )
                    )
                )
                res.append(ms)
                val = (len(res[index]) / (1.0 * len(self._etalon[index]))) * 100
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(len(self._etalon[index]))
                                         + " Positive: " + str(len(res[index])) + " Probability: " + str(val) +
                                         " (Weight: " + str(len(et_cluster) / (1.0 * summ)) + ")")
                prob += (len(et_cluster) / (1.0 * summ)) * val
            else:
                res.append(ms)
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(len(self._etalon[index]))
                                         + " Invalid.")
        logger.algo_logger.debug("Probability: " + str(prob))
        return prob
