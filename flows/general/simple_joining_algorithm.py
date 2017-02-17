from base import IAlgorithm


class SimpleJoiningAlgorithm(IAlgorithm):
    def __init__(self, joining_key=None):
        self._key = joining_key

    def apply(self, data):
        if data is not None and isinstance(data, list):
            active_key = data[0].get('active', None)
            join_key = self._key
            if join_key is None:
                join_key = active_key[0] if active_key is not None else 'data'
            joined_data = []
            for jdata in data:
                join_data = jdata.get(join_key, None)
                joined_data.append(join_data)
            joined = data[0].copy()
            joined[join_key] = joined_data
            return joined
        return data
