from ..wnearpyhash import wNearPyHash
import numpy


def wNearPyHash_test():
    nearpy_hash = wNearPyHash()
    assert nearpy_hash is not None
    assert nearpy_hash.type() == "wNearPyHash"
    assert nearpy_hash.hash_list() == ['rbp']
    test_vector = numpy.random.random(32)
    assert nearpy_hash.hash_vectors([test_vector]) is not None
    assert len(nearpy_hash.hash_vector(test_vector)) == 1
    assert nearpy_hash.neighbours(test_vector) == []
    assert nearpy_hash.get_config() is not None
