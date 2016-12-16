from ..rectfilter import filterRectangles


def filterRectangles_test():
    rects = [[0, 3, 10, 15], [5, 10, 20, 10], [15, 20, 100, 50], [10, 10, 30, 40]]
    res = filterRectangles(rects)
    assert res is not None
    assert res == [15, 20, 100, 50]
