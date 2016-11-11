from ..kmeans import get_cluster, KMeans
import cv2


def KMeans_test():
    keypoints = [cv2.KeyPoint(0.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(0.0, 5.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 5.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(3.0, 3.0, 14.2, 0.0, 2.3112, 0, -1)]
    res = KMeans(keypoints, 4)
    assert res is not None
    assert len(res) == 4
    for r in res:
        assert r.has_key('items')
        assert r.has_key('center')
    res = KMeans(keypoints, 4, [(1, 1), (5, 1), (1, 6), (3, 3)])
    assert res is not None
    assert len(res) == 4
    for r in res:
        assert 'items' in r
        assert 'center' in r
