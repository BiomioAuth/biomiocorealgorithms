from ..strategies import ROIManagementStrategy, ROICenterStrategy, ROIFilteringStrategy, ROIIncludeStrategy, \
    ROIIntersectionStrategy, ROIPositionStrategy, ROISizingStrategy, ROIUnionStrategy, StrategyFactory


def ROIManagementStrategy_test():
    strategy = ROIManagementStrategy()
    assert strategy is not None
    assert strategy.type() == "none"
    assert strategy.apply([]) == []


def ROIIntersectionStrategy_test():
    strategy = ROIIntersectionStrategy()
    assert strategy is not None
    assert strategy.type() == "intersection"
    rects = [[0, 1, 5, 3], [2, 0, 3, 5], [3, 2, 3, 3], [3, 3, 4, 4]]
    res = strategy.apply(rects)
    assert res is not None
    assert res == [3, 3, 2, 1]


def ROIUnionStrategy_test():
    strategy = ROIUnionStrategy()
    assert strategy is not None
    assert strategy.type() == "union"
    rects = [[0, 1, 5, 3], [2, 0, 3, 5], [3, 2, 3, 3], [3, 3, 4, 4]]
    res = strategy.apply(rects)
    assert res is not None
    assert res == [[0, 0, 7, 7]]


def ROIFilteringStrategy_test():
    strategy = ROIFilteringStrategy()
    assert strategy is not None
    assert strategy.type() == "filtering"
    rects = [[0, 3, 10, 15], [5, 10, 20, 10], [15, 20, 100, 50], [10, 10, 30, 40]]
    res = strategy.apply(rects)
    assert res is not None
    assert res == [[15, 20, 100, 50]]


def ROIPositionStrategy_test():
    settings = {'kind': 'min', 'template': 1, 'pos': 0.5}
    strategy = ROIPositionStrategy(settings)
    assert strategy is not None
    assert strategy.type() == "position"
    rects = [[0, 3, 100, 150], [5, 100, 20, 10], [15, 20, 10, 50], [10, 150, 30, 40]]
    res = strategy.apply(rects)
    assert res is not None
    res = res[0]
    assert res[0] == rects[0]
    assert res[1] == rects[2]
    settings = {'kind': 'max_center', 'template': 1, 'pos': 0.5}
    strategy = ROIPositionStrategy(settings)
    res = strategy.apply(rects)
    assert res is not None
    res = res[0]
    assert res[0] == rects[0]
    assert res[1] == rects[1]


def ROICenterStrategy_test():
    strategy = ROICenterStrategy({'distance': 0.3})
    assert strategy is not None
    assert strategy.type() == "center"
    rects = [[0, 3, 100, 150], [5, 100, 20, 10], [15, 20, 10, 50], [10, 15, 80, 100]]
    res = strategy.apply(rects)
    assert res is not None
    assert res[0] == rects[3]


def ROIIncludeStrategy_test():
    strategy = ROIIncludeStrategy()
    assert strategy is not None
    assert strategy.type() == "include"
    rects = [[0, 3, 100, 150], [5, 100, 20, 10], [15, 20, 10, 50], [10, 150, 30, 40]]
    res = strategy.apply(rects)
    assert res is not None
    assert res[0] == rects[1]
    assert res[1] == rects[2]


def ROISizingStrategy_test():
    strategy = ROISizingStrategy({'scale': 0.5, 'kind': 'max'})
    assert strategy is not None
    assert strategy.type() == "sizing"
    rects = [[0, 3, 100, 150], [5, 100, 20, 10], [15, 20, 10, 50], [10, 150, 30, 40]]
    res = strategy.apply(rects)
    assert res is not None
    assert res[0] == rects[0]

	
def ROIScaleStrategy_test():
    return False


def StrategyFactory_test():
    factory = StrategyFactory()
    assert factory is not None
    assert StrategyFactory.get({'type': "union", 'settings': {}}) is not None
    assert StrategyFactory.get({'type': "position", 'settings': {}}) is not None
    assert StrategyFactory.get({'type': "sizing", 'settings': {}}) is not None
