from ..nearpyhash import NearPyHashSettings, NearPyHash, RandomBinaryProjections, ManhattanDistance, xMemoryStorage
import numpy


def NearPyHashSettings_test():
    settings = NearPyHashSettings()
    assert settings is not None
    assert settings.projection == RandomBinaryProjections
    assert settings.projection_name == 'rbp'
    assert settings.projection_count == 10
    assert settings.dimension == 32
    assert settings.distance == ManhattanDistance
    assert settings.detector is None
    assert settings.threshold == 0.25
    assert settings.storage == xMemoryStorage


def NearPyHash_test():
    nearpy_hash = NearPyHash(NearPyHashSettings())
    assert nearpy_hash is not None
    assert nearpy_hash.type() == "NearPyHash"
    test_vector = numpy.random.random(32)
    assert len(nearpy_hash.store_vector(test_vector)) == 1
    assert len(nearpy_hash.store_vectors([test_vector])) == 1
    assert nearpy_hash.candidate_count(test_vector) == 2
    res = nearpy_hash.neighbours(test_vector)
    assert res is not None
    assert res[0][2] == 0.0
    nearpy_hash.clean_buckets("rbp")
    nearpy_hash.clean_all_buckets()
    nearpy_hash.clean_vectors_by_data("rbp", None)
    nearpy_hash.clean_all_vectors("rbp", None)
    nearpy_hash.dump()
