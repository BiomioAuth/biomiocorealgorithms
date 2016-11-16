from ..verification_collector import VerificationCollector
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
STAT_LOG_PATH = os.path.join(scriptDir, "test_data", "stat.log")


def VerificationCollector_test():
    data = {
        'data': [],
        'logfile': STAT_LOG_PATH,
        'logdata': scriptDir,
        'collection_dir': scriptDir
    }
    collector = VerificationCollector()
    assert collector is not None
    collector.apply(data)
    os.remove(os.path.join(scriptDir, "stat.log"))
