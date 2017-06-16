from biomio.algorithms.algorithms.cvtools.system import saveNumpyImage, loadNumpyImage
import tempfile
import json
import os


def save_temp_data(data, path, images=[]):
    if path:
        fd, temp_file = tempfile.mkstemp(dir=path)
        os.close(fd)
        for image in images:
            im_path = temp_file + '_' + image + ".png"
            saveNumpyImage(im_path, data[image])
            data[image] = im_path
        data['save'] = images
        json_encoded = json.dumps(data)
        with open(temp_file, 'w') as f:
            f.write(json_encoded)
            f.close()
        return temp_file
    return path


def load_temp_data(path, remove=True, load_saved=True):
    source = dict()
    if os.path.exists(path):
        with open(path, "r") as data_file:
            source = json.load(data_file)
        data_file.close()
        if remove:
            os.remove(path)
        if load_saved:
            saved = source.get('save', None)
            if saved is not None:
                for im in saved:
                    img = loadNumpyImage(source[im])
                    if remove:
                        os.remove(source[im])
                    source[im] = img
    return source


def remove_temp_data(path):
    if os.path.exists(path):
        with open(path, "r") as data_file:
            source = json.load(data_file)
        data_file.close()
        os.remove(path)
        saved = source.get('save', None)
        if saved is not None:
            for im in saved:
                os.remove(source[im])


def remove_temp_data(path):
    if os.path.exists(path):
        os.remove(path)
