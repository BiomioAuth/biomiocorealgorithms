from ..emptyfilter import EmptyFilter
import numpy


def EmptyFilter_test():
    filter = EmptyFilter()
    test_ndarray = numpy.zeros((10), dtype=numpy.float32)
    assert numpy.array_equal(filter.filter_vectors(test_ndarray), test_ndarray)
