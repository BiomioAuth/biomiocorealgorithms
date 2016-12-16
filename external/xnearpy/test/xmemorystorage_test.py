from ..xmemorystorage import xMemoryStorage


def xMemoryStorage_test():
    storage = xMemoryStorage()
    assert storage is not None
    storage.clean_vectors_by_data("rbp", None)
    storage.clean_all_vectors("rbp", None)
