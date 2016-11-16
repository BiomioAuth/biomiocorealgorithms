from ..image_error_collector import ImageErrorCollector
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
ERROR_LOG_PATH = os.path.join(scriptDir, "test_data", "error.log")


def ImageErrorCollector_test():
    data = {
        'data': [],
        'logfile': ERROR_LOG_PATH,
        'logdata': scriptDir,
        'collection_dir': scriptDir
    }
    collector = ImageErrorCollector()
    assert collector is not None
    collector.apply(data)
    os.remove(os.path.join(scriptDir, "error.log"))
