from ..tools import distance, mass_center, sort_clusters, get_cluster
import cv2


def get_cluster_test():
    d_id = 10
    d_center = (3, 2)
    d_items = []
    test_dict = {'center': d_center, 'items': d_items, 'id': d_id}
    res = get_cluster(d_id, d_center, d_items)
    assert res is not None
    assert test_dict == res


def distance_test():
    res = distance((0, 0), (2, 2))
    assert res is not None
    assert int(res**2) == int(8.0)


def mass_center_test():
    keypoints = [cv2.KeyPoint(0.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(0.0, 5.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 5.0, 14.2, 0.0, 2.3112, 0, -1)]
    res = mass_center(keypoints)
    assert res is not None
    assert res == (2.5, 2.5)


def sort_clusters_test():
    clusters = [get_cluster(1, (0, 3), []), get_cluster(4, (0, 6), []),
                get_cluster(0, (0, 0), []), get_cluster(3, (1, 1), [])]
    res = sort_clusters(clusters)
    assert res is not None
    c_id = -1
    for r in res:
        assert c_id < r['id']
        c_id = r['id']
