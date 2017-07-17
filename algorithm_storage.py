from threading import Lock


class AlgorithmStorage:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._storage = {}

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = AlgorithmStorage()
        return cls._instance

    def exists(self, key):
        """
        Check if existing object key exists.
        
        :param str key: Object key.
        :return: True if key exists; False otherwise.
        :rtype: bool
        """
        return self._storage.__contains__(key)

    def get(self, key):
        """
        Return algorithm object from storage by specified key.
        
        :param str key: Object key.
        :return: Object instance.
        """
        return self._storage.get(key, None)

    def register(self, key, obj):
        """
        Store object into storage.
        
        :param str key: Object key.
        :param ref obj: Object instance.
        """
        if obj is not None:
            self._storage[key] = obj
