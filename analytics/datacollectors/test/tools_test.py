from ..tools import get_files, get_dirs, file_map, dir_map
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_FOLDER = os.path.join(scriptDir, "..")


def get_files_test():
    files = get_files(TEST_FOLDER)
    assert len(files) == 8


def get_dirs_test():
    dirs = get_dirs(TEST_FOLDER)
    assert len(dirs) == 1


def file_map_test():
    fmap = file_map(TEST_FOLDER)
    assert len(fmap.keys()) == 16


def dir_map_test():
    fmap = dir_map(TEST_FOLDER)
    assert len(fmap.keys()) == 2
