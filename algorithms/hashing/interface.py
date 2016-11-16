class DataStructure:
    def __init__(self, settings):
        self.init_structure(settings)

    def init_structure(self, settings):
        pass

    def store_vector(self, v, data=[]):
        raise NotImplementedError

    def store_vectors(self, vs):
        raise NotImplementedError

    def clean_all_buckets(self):
        raise NotImplementedError

    def clean_vectors_by_data(self, hash_name, data, bucket_keys=[]):
        raise NotImplementedError

    def clean_all_vectors(self, hash_name, data):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError
