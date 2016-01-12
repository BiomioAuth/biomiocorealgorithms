from biomio.algorithms.features import matcherForDetector, dtypeForDetector
from biomio.algorithms.interfaces import AlgorithmEstimation, logger
from biomio.algorithms.cvtools.types import listToNumpy_ndarray
from biomio.algorithms.features.matchers import Matcher
import itertools
import math

DEFAULT_MODE = 0
CROSS_DISTANCE_MODE = 1
FULL_DISTANCE_MODE = 2


class ClusterL0Estimation(AlgorithmEstimation):
    def __init__(self, detector_type, knn, mode=DEFAULT_MODE):
        self._mode = mode
        self._knn = knn
        self._matcher = Matcher(matcherForDetector(detector_type))
        self._dtype = dtypeForDetector(detector_type)

    def estimate_training(self, data, database):
        template = database
        if len(database) == 0:
            template = data
        else:
            for index, et_cluster in enumerate(database):
                dt_cluster = data[index]
                if et_cluster is None or len(et_cluster) == 0 or len(et_cluster) < self._knn:
                    template[index] = et_cluster
                elif dt_cluster is None or len(dt_cluster) == 0 or len(dt_cluster) < self._knn:
                    template[index] = et_cluster
                else:
                    matches1 = self._matcher.knnMatch(listToNumpy_ndarray(et_cluster, self._dtype),
                                                      listToNumpy_ndarray(dt_cluster, self._dtype), k=self._knn)
                    matches2 = self._matcher.knnMatch(listToNumpy_ndarray(dt_cluster, self._dtype),
                                                      listToNumpy_ndarray(et_cluster, self._dtype), k=self._knn)
                    good = list(itertools.chain.from_iterable(itertools.imap(
                        lambda(x, _): (et_cluster[x.queryIdx], dt_cluster[x.trainIdx]), itertools.ifilter(
                            lambda(m, n): m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx, itertools.product(
                                itertools.chain(*matches1), itertools.chain(*matches2)
                            )
                        )
                    )))
                    template[index] = listToNumpy_ndarray(good)
        return template

    def estimate_verification(self, data, database):
        prob = 0
        logger.debug("Template size: ")
        summ = sum(itertools.imap(lambda x: len(x) if x is not None else 0, database))
        for index, et_cluster in enumerate(database):
            dt_cluster = data[index]
            if et_cluster is None or len(et_cluster) < self._knn:
                logger.debug("Cluster #" + str(index + 1) + ": " + str(-1) + " Invalid. (Weight: 0)")
                continue
            if dt_cluster is None or len(dt_cluster) < self._knn:
                logger.debug("Cluster #" + str(index + 1) + ": " + str(len(database[index]))
                             + " Positive: 0 Probability: 0 (Weight: " + str(len(et_cluster) / (1.0 * summ)) + ")")
                continue
            if len(et_cluster) > 0 and len(dt_cluster) > 0:
                matches1 = self._matcher.knnMatch(listToNumpy_ndarray(et_cluster, self._dtype),
                                                  listToNumpy_ndarray(dt_cluster, self._dtype), k=self._knn)
                matches2 = self._matcher.knnMatch(listToNumpy_ndarray(dt_cluster, self._dtype),
                                                  listToNumpy_ndarray(et_cluster, self._dtype), k=self._knn)
                ml = [
                    x for (x, _) in itertools.ifilter(
                        lambda(m, n): m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx, itertools.product(
                            itertools.chain(*matches1), itertools.chain(*matches2)
                        )
                    )
                ]
                ms = len(ml)
                if self._mode == CROSS_DISTANCE_MODE:
                    ms = sum([1/math.exp(m.distance) for m in ml])
                elif self._mode == FULL_DISTANCE_MODE:
                    mu = [
                        x for (x, _) in itertools.ifilter(
                            lambda(m, n): m.queryIdx != n.trainIdx or m.trainIdx != n.queryIdx, itertools.product(
                                itertools.chain(*matches1), itertools.chain(*matches2)
                            )
                        )
                    ]
                    ms = sum([2/math.exp(m.distance) for m in ml]) + sum([1/math.exp(m.distance) for m in mu])
                logger.debug(ms)
                val = (ms / (1.0 * len(et_cluster))) * 100
                logger.debug("Cluster #" + str(index + 1) + ": " + str(len(et_cluster)) + " Positive: "
                             + str(ms) + " Probability: " + str(val) + " (Weight: "
                             + str(len(et_cluster) / (1.0 * summ)) + ")")
                prob += (len(et_cluster) / (1.0 * summ)) * val
            else:
                logger.debug("Cluster #" + str(index + 1) + ": " + str(len(et_cluster)) + " Invalid.")
        logger.debug("Probability: " + str(prob))
        return prob
