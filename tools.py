import json
import os

def load_json(path):
    if not os.path.exists(path):
        return dict()
    with open(path, "r") as data_file:
        source = json.load(data_file)
        return source

def save_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
    return True
