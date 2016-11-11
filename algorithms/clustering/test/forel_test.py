from ..forel import FOREL, neighbour_objects
import cv2


def FOREL_test():
    keypoints = [cv2.KeyPoint(0.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(0.0, 5.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 5.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(3.0, 3.0, 14.2, 0.0, 2.3112, 0, -1)]
    res = FOREL(keypoints, 3)
    assert res is not None
    assert len(res) == 4
    for r in res:
        assert 'items' in r
        assert 'center' in r


def neighbour_objects_test():
    keypoints = [cv2.KeyPoint(0.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 0.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(0.0, 5.0, 14.2, 0.0, 2.3112, 0, -1),
                 cv2.KeyPoint(5.0, 5.0, 14.2, 0.0, 2.3112, 0, -1)]
    res = neighbour_objects(keypoints, (3, 3), 3)
    assert res is not None
    assert res[0].pt == (5.0, 5.0)
