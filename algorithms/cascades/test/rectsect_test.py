from ..rectsect import intersectRectangles


def intersectRectangles_test():
    rects = [[0, 1, 5, 3], [2, 0, 3, 5], [3, 2, 3, 3], [3, 3, 4, 4]]
    res = intersectRectangles(rects)
    assert res is not None
    assert res == [3, 3, 2, 1]
