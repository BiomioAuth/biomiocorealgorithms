from biomio.algorithms.flows.base import IAlgorithm
from shutil import copyfile
from tools import file_map
import os

class ImageErrorCollector(IAlgorithm):
    def __init__(self):
        pass

    def apply(self, data):
        if data is None:
            return None
        data_map = None
        logpath = os.path.split(data['logfile'])[0]
        if not os.path.exists(data['collection_dir']):
            os.makedirs(data['collection_dir'])
        copyfile(data['logfile'], os.path.join(data['collection_dir'], os.path.split(data['logfile'])[1]))
        for log_item in data['data']:
            path = log_item['path'] if os.path.exists(log_item['path']) else None
            adpath, filepath = os.path.split(log_item['path'])
            if path is None:
                adpath, dirpath = os.path.split(adpath)
                basepath = os.path.split(adpath)[1]
                if data.get('logdata', None) is not None:
                    path = os.path.join(data['logdata'], basepath, dirpath, filepath)
                if not os.path.exists(path):
                    path = os.path.join(logpath, basepath, dirpath, filepath)
            if not os.path.exists(path):
                if data_map is None:
                    map_path = logpath if data.get('logdata', None) is None else data['logdata']
                    data_map = file_map(map_path) if os.path.exists(map_path) else {}
                path = data_map.get(filepath, None)
            if path is None or not os.path.exists(path):
                print('Logged File {} not found!'.format(path))
            else:
                copyfile(path, os.path.join(data['collection_dir'], filepath))
