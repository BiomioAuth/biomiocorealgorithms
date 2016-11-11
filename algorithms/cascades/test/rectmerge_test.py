from ..rectmerge import mergeRectangles


def mergeRectangles_test():
    rects = [[0, 1, 5, 3], [2, 0, 3, 5], [3, 2, 3, 3], [3, 3, 4, 4]]
    res = mergeRectangles(rects)
    assert res is not None
    assert res == [0, 0, 7, 7]