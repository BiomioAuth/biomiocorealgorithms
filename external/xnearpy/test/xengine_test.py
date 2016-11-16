from ..xengine import xEngine
import numpy


def xEngine_test():
    engine = xEngine(32)
    assert engine is not None
    test_vector = numpy.random.random(32)
    assert len(engine.store_vector(test_vector)) == 1
    assert len(engine.store_vectors([test_vector])) == 1
    engine.clean_vectors_by_data("rbp", None)
    engine.clean_all_vectors("rbp", None)
