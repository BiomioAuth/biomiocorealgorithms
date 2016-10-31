from nearpy.distances import EuclideanDistance, ManhattanDistance
from ...external.xnearpy.xmemorystorage import xMemoryStorage
from nearpy.hashes import RandomBinaryProjections
from ...external.xnearpy.xengine import xEngine
from interface import DataStructure


class NearPyHashSettings:
    def __init__(self):
        self.projection = RandomBinaryProjections
        self.projection_name = "rbp"
        self.projection_count = 10
        self.dimension = 32
        self.distance = ManhattanDistance
        self.detector = None
        self.threshold = 0.25
        self.storage = xMemoryStorage


class NearPyHash(DataStructure):
    def __init__(self, settings):
        self.engine = None
        DataStructure.__init__(self, settings)

    @staticmethod
    def type():
        return "NearPyHash"

    def init_structure(self, settings, storage=None):
        projection = settings.projection(settings.projection_name, settings.projection_count)
        self.engine = xEngine(settings.dimension, lshashes=[projection], distance=settings.distance(),
                              storage=storage)

    def store_vector(self, v, data=None):
        return self.engine.store_vector(v, data)

    def store_vectors(self, vs, data=None):
        return self.engine.store_vectors(vs, data)

    def candidate_count(self, v):
        return self.engine.candidate_count(v)

    def neighbours(self, v):
        return self.engine.neighbours(v)

    def clean_buckets(self, hash_name):
        self.engine.clean_buckets(hash_name)

    def clean_all_buckets(self):
        self.engine.clean_all_buckets()

    def clean_vectors_by_data(self, hash_name, data, bucket_keys=[]):
        self.engine.clean_vectors_by_data(hash_name, data, bucket_keys)

    def clean_all_vectors(self, hash_name, data):
        self.engine.clean_all_vectors(hash_name, data)

    def dump(self):
        self.engine.dump()
