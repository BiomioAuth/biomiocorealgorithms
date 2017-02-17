from base import IAlgorithm


class SimpleSeparationAlgorithm(IAlgorithm):
    def __init__(self, separation_key=None):
        self._key = separation_key

    def apply(self, data):
        if data is not None:
            active_key = data.get('active', None)
            split_key = self._key
            if split_key is None:
                split_key = active_key[0] if active_key is not None else 'data'
            split_data = data.get(split_key, None)
            if split_data is not None:
                splitted = []
                for sdata in split_data:
                    pair_data = data.copy()
                    pair_data[split_key] = sdata
                    splitted.append(pair_data)
                return splitted
            return [data]
        return data
