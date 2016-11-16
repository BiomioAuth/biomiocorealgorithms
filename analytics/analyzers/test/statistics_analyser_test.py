from ...dataformats.verification_result_format import VerificationResultFormat
from ...datacollectors.verification_collector import VerificationCollector
from ...datacollectors.image_error_collector import ImageErrorCollector
from ...dataformats.image_error_format import ImageErrorFormat
from ..statistics_analyser import StatisticsAnalyser
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
ERROR_LOG_PATH = os.path.join(scriptDir, "test_data", "error.log")
STAT_LOG_PATH = os.path.join(scriptDir, "test_data", "stat.log")


def StatisticsAnalyser_test():
    sanalyser = StatisticsAnalyser(ImageErrorFormat(), ImageErrorCollector())
    assert sanalyser is not None
    sanalyser.parse(scriptDir, ERROR_LOG_PATH, scriptDir)

    resultanalyser = StatisticsAnalyser(VerificationResultFormat(), VerificationCollector())
    assert resultanalyser is not None
    resultanalyser.parse(scriptDir, STAT_LOG_PATH, scriptDir)
    os.remove(os.path.join(scriptDir, "error.log"))
    os.remove(os.path.join(scriptDir, "stat.log"))

