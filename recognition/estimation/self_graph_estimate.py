from biomio.algorithms.cvtools.types import listToNumpy_ndarray
from base_template_estimate import BaseTemplateEstimation
from biomio.algorithms.logger import logger
import numpy as np
import itertools
import copy


class SelfGraphEstimation(BaseTemplateEstimation):
    def __init__(self, detector_type, knn):
        BaseTemplateEstimation.__init__(self, detector_type, knn)

    def estimate_verification(self, data, database):
        prob = 0
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
                        lambda (m, n): m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx, itertools.product(
                            itertools.chain(*matches1), itertools.chain(*matches2)
                        )
                    )
                ]
                # corr_nodes = [(et_cluster[m.queryIdx], dt_cluster[m.trainIdx]) for m in ml]
                corr_nodes = []
                for m in ml:
                    unique = True
                    for item in corr_nodes:
                        if (np.array_equal(item[0], et_cluster[m.queryIdx]) or
                                np.array_equal(item[1], dt_cluster[m.trainIdx])):
                            if item[2] > m.distance:
                                item[0] = et_cluster[m.queryIdx]
                                item[1] = dt_cluster[m.trainIdx]
                                item[2] = m.distance
                            unique = False
                    if unique:
                        corr_nodes.append([et_cluster[m.queryIdx], dt_cluster[m.trainIdx], m.distance])
                et_nodes = [m[0] for m in corr_nodes]
                dt_nodes = [m[1] for m in corr_nodes]
                et_self_match = self._self_matching(et_nodes)
                dt_self_match = self._self_matching(dt_nodes)
                # self._print_data(corr_nodes, et_self_match, dt_self_match)
                et_normal = 0
                dt_normal = 0
                end = False
                for corr in corr_nodes:
                    for et_pair in et_self_match:
                        if np.array_equal(corr[0], et_pair[0]):
                            for dt_pair in dt_self_match:
                                if np.array_equal(corr[1], dt_pair[0]):
                                    for c in corr_nodes:
                                        if np.array_equal(c[0], et_pair[1]) and np.array_equal(c[1], dt_pair[1]):
                                            et_normal = et_pair[2]
                                            dt_normal = dt_pair[2]
                                            end = True
                                            break
                                if end:
                                    break
                        if end:
                            break
                    if end:
                        break
                for et_pair in et_self_match:
                    et_pair[2] /= 1.0 * et_normal
                for dt_pair in dt_self_match:
                    dt_pair[2] /= 1.0 * dt_normal
                # self._print_data(corr_nodes, et_self_match, dt_self_match)
                c_prob = 0
                # for corr in corr_nodes:
                #     for et_pair in et_self_match:
                #         if np.array_equal(corr[0], et_pair[0]):
                #             for dt_pair in dt_self_match:
                #                 if np.array_equal(corr[1], dt_pair[0]):
                #                     for c in corr_nodes:
                #                         if np.array_equal(c[0], et_pair[1]) and np.array_equal(c[1], dt_pair[1]):
                #                             if et_pair[2] > dt_pair[2]:
                #                                 c_prob += dt_pair[2] / et_pair[2]
                #                             else:
                #                                 c_prob += et_pair[2] / dt_pair[2]
                #                             break
                for et_pair in et_self_match:
                    end = False
                    for corr in corr_nodes:
                        if np.array_equal(corr[0], et_pair[0]):
                            for c in corr_nodes:
                                if np.array_equal(c[0], et_pair[1]):
                                    for dt_pair in dt_self_match:
                                        if np.array_equal(corr[1], dt_pair[0]) and np.array_equal(c[1], dt_pair[1]):
                                            coeff = 0
                                            if corr[2] == c[2] == 0:
                                                coeff = 1
                                            elif corr[2] > c[2]:
                                                coeff = c[2] / corr[2]
                                            else:
                                                coeff = corr[2] / c[2]
                                            if et_pair[2] > dt_pair[2]:
                                                c_prob += coeff * (dt_pair[2] / et_pair[2])
                                            else:
                                                c_prob += coeff * (et_pair[2] / dt_pair[2])
                                            end = True
                                            break
                                    if end:
                                        break
                            if end:
                                break
                val = (c_prob / (1.0 * len(et_self_match))) * 100 # * (len(ml) / (1.0 * len(et_cluster)))
                logger.debug("Cluster #" + str(index + 1) + ": " + str(len(et_self_match)) + " Positive: "
                             + str(c_prob) + " Probability: " + str(val)
                             + " (Weight: " + str(len(et_cluster) / (1.0 * summ)) + ")"
                             )
                prob += (len(et_cluster) / (1.0 * summ)) * val
                # prob += val
            else:
                logger.debug("Cluster #" + str(index + 1) + ": " + str(len(et_cluster)) + " Invalid.")
        # prob /= 1.0 * len(database)
        logger.debug("Probability: " + str(prob))
        return prob

    def _self_matching(self, descriptors):
        self_match = []
        for desc in descriptors:
            query_set = [desc]
            train_set = [d for d in descriptors if not np.array_equal(desc, d)]
            s_match = self._matcher.knnMatch(listToNumpy_ndarray(query_set, self._dtype),
                                             listToNumpy_ndarray(train_set, self._dtype), k=self._knn)
            for m in itertools.chain(*s_match):
                self_match.append([query_set[m.queryIdx], train_set[m.trainIdx], m.distance])
        return self_match

    def _print_data(self, corr_nodes, et_matches, dt_matches):
        desc_list = []
        corr_nodes_copy = copy.deepcopy(corr_nodes)
        et_matches_copy = copy.deepcopy(et_matches)
        dt_matches_copy = copy.deepcopy(dt_matches)
        for corr in corr_nodes_copy:
            corr_first = -1
            corr_second = -1
            for desc in desc_list:
                if np.array_equal(desc[0], corr[0]):
                    corr_first = desc[1]
                if np.array_equal(desc[0], corr[1]):
                    corr_second = desc[1]
                if corr_first >= 0 and corr_second >= 0:
                    break
            if corr_first < 0:
                corr_first = len(desc_list)
                desc_list.append((corr[0], corr_first))
            corr[0] = corr_first
            if corr_second < 0:
                corr_second = len(desc_list)
                desc_list.append((corr[1], corr_second))
            corr[1] = corr_second
        for et in et_matches_copy:
            corr_first = -1
            corr_second = -1
            for desc in desc_list:
                if np.array_equal(desc[0], et[0]):
                    corr_first = desc[1]
                if np.array_equal(desc[0], et[1]):
                    corr_second = desc[1]
                if corr_first >= 0 and corr_second >= 0:
                    break
            if corr_first < 0:
                corr_first = len(desc_list)
                desc_list.append((et[0], corr_first))
            et[0] = corr_first
            if corr_second < 0:
                corr_second = len(desc_list)
                desc_list.append((et[1], corr_second))
            et[1] = corr_second
        for dt in dt_matches_copy:
            corr_first = -1
            corr_second = -1
            for desc in desc_list:
                if np.array_equal(desc[0], dt[0]):
                    corr_first = desc[1]
                if np.array_equal(desc[0], dt[1]):
                    corr_second = desc[1]
                if corr_first >= 0 and corr_second >= 0:
                    break
            if corr_first < 0:
                corr_first = len(desc_list)
                desc_list.append((dt[0], corr_first))
            dt[0] = corr_first
            if corr_second < 0:
                corr_second = len(desc_list)
                desc_list.append((dt[1], corr_second))
            dt[1] = corr_second
        # logger.debug("######################################")
        # logger.debug(desc_list)
        logger.debug("######################################")
        logger.debug(corr_nodes_copy)
        logger.debug("######################################")
        logger.debug(et_matches_copy)
        logger.debug("######################################")
        logger.debug(dt_matches_copy)
        logger.debug("######################################")
