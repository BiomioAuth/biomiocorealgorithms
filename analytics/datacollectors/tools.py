import os


###################################################################################################
# Python Filesystem Extras - File Searching
# import os
def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
###################################################################################################


###################################################################################################
# Python Filesystem Extras - Directory Searching
# import os
def get_dirs(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
###################################################################################################


def file_map(path):
    result = {}
    if os.path.exists(path):
        onlydirs = get_dirs(path)
        for rel_dir in onlydirs:
            result.update(file_map(os.path.join(path, rel_dir)))
        onlyfiles = get_files(path)
        for rel_file in onlyfiles:
            result[rel_file] = os.path.join(path, rel_file)
    return result


def dir_map(path):
    result = {}
    if os.path.exists(path):
        onlydirs = get_dirs(path)
        for rel_dir in onlydirs:
            result.update(dir_map(os.path.join(path, rel_dir)))
            result[rel_dir] = os.path.join(path, rel_dir)
    return result
