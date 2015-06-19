from __future__ import absolute_import
import logger
from biomio.algorithms.algorithms.features.matchers import Matcher, BruteForceMatcherType
from biomio.algorithms.algorithms.recognition.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.algorithms.recognition.keypoints import (listToNumpy_ndarray, numpy_ndarrayToList,
                                                                verifying)
import numpy


class ClustersDBMatchingDetector(ClustersMatchingDetector):
    def __init__(self):
        ClustersMatchingDetector.__init__(self)

    def update_hash(self, data):
        del data['keypoints']
        del data['descriptors']
        self._hash.append(data)

    def importSources(self, source):
        self._etalon = []
        logger.algo_logger.debug("Database loading started...")
        self.importSources_Database(source.get('data', dict()))
        self._prob = source.get('threshold', 100)
        logger.algo_logger.debug("Database loading finished.")

    def importSources_Database(self, source):
        for j in range(0, len(source.keys())):
            self._hash.append(dict())
        for c_num, item in source.iteritems():
            item_data = [[] for key in item.keys()]
            for d_num, cluster in item.iteritems():
                desc = [[] for c_key in cluster.keys()]
                for e_num, descriptor in cluster.iteritems():
                    desc[int(e_num)] = listToNumpy_ndarray(descriptor)
                item_data[int(d_num)] = desc
            obj = dict()
            obj["clusters"] = item_data
            self._hash[int(c_num) - 1] = obj

    def exportSources(self):
        data = self.exportSources_Database()
        source = dict()
        if len(data.keys()) > 0:
            source['data'] = data
            source['threshold'] = self._prob
        return source

    def exportSources_Database(self):
        etalon = dict()
        i = 0
        for data in self._hash:
            i += 1
            elements = dict()
            for index in range(0, len(data["clusters"])):
                cluster = data["clusters"][index]
                desc = dict()
                if cluster is not None:
                    for indx in range(0, len(cluster)):
                        desc[indx] = numpy_ndarrayToList(cluster[indx])
                elements[str(index)] = desc
            etalon[str(i)] = elements
        return etalon

    @verifying
    def verify(self, data):
        matcher = Matcher(BruteForceMatcherType)
        gres = []
        for d in self._hash:
            res = []
            for i in range(0, len(d['clusters'])):
                test = data['clusters'][i]
                source = d['clusters'][i]
                if (test is None) or (source is None) or (len(test) == 0) or (len(source) == 0):
                    logger.algo_logger.debug("Cluster #" + str(i + 1) + ": Invalid")
                else:
                    matches = matcher.knnMatch(listToNumpy_ndarray(test, numpy.uint8),
                                               listToNumpy_ndarray(source, numpy.uint8), k=1)
                    ms = []
                    # TODO: I think, this for can be modified. Do you have some idea?
                    for v in matches:
                        if len(v) >= 1:
                            m = v[0]
                            if m.distance < self.kodsettings.neighbours_distance:
                                ms.append(m)
                    prob = len(ms) / (1.0 * len(matches))
                    res.append(prob * 100)
                    logger.algo_logger.debug("Cluster #" + str(i + 1) + " (Size: " + str(len(source)) + "): "
                                             + str(prob * 100) + "%")
            suma = sum(res)
            logger.algo_logger.debug("Total for image: " + str(suma / len(res)))
            gres.append(suma / len(res))
        s = sum(gres)
        logger.algo_logger.debug("Total: " + str(s / len(gres)))
        return s / len(gres)
