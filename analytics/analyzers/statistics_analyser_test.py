import os

from analytics.analyzers.statistics_analyser import StatisticsAnalyser
from analytics.datacollectors import ImageErrorCollector, VerificationCollector
from analytics.dataformats import ImageErrorFormat, VerificationResultFormat

MAIN_OUT_ERR_LOG_PATH = "D:/Projects/Biomio/Test1/AnalyticsDB/ErrorDB"
MAIN_OUT_STAT_LOG_PATH = "D:/Projects/Biomio/Test1/AnalyticsDB/StatDB"

DATA_FILES_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.28/prototype-protocol/openface_vp/"
PARSED_DATA_DIR = "16.07.28/prototype-protocol/openface_vp"
ERROR_LOG_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.28/prototype-protocol/openface_vp/error.log"
STAT_LOG_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.28/prototype-protocol/openface_vp/stat.log"
# PARSED_RES_LOG_PATH = "D:/Projects/Biomio/Test1/FaceDB/parsed_data"

# STAT_LOG2_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.13/prod_photo/stat.log"
# DATA_FILES2_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.13/prod_photo"
# PARSED_RES_LOG2_PATH = "D:/Projects/Biomio/Test1/FaceDB/parsed_data2"

def run():
    sanalyser = StatisticsAnalyser(ImageErrorFormat(), ImageErrorCollector())
    sanalyser.parse(os.path.join(MAIN_OUT_ERR_LOG_PATH, PARSED_DATA_DIR), ERROR_LOG_PATH, DATA_FILES_PATH)

    resultanalyser = StatisticsAnalyser(VerificationResultFormat(), VerificationCollector())
    resultanalyser.parse(os.path.join(MAIN_OUT_STAT_LOG_PATH, PARSED_DATA_DIR), STAT_LOG_PATH, DATA_FILES_PATH)

if __name__ == '__main__':
    run()
