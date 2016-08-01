from datacollectors import ImageErrorCollector, VerificationCollector
from dataformats import ImageErrorFormat, VerificationResultFormat
from statistics_analyser import StatisticsAnalyser

DATA_FILES_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.13/dev_photo/openface_pl/"
ERROR_LOG_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.13/dev_photo/openface_pl/error.log"
PARSED_LOG_PATH = "D:/Projects/Biomio/Test1/FaceDB/parsed_error"
STAT_LOG_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.13/dev_photo/openface_pl/stat.log"
PARSED_RES_LOG_PATH = "D:/Projects/Biomio/Test1/FaceDB/parsed_data"

STAT_LOG2_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.13/prod_photo/stat.log"
DATA_FILES2_PATH = "D:/Projects/Biomio/Test1/FaceDB/16.07.13/prod_photo"
PARSED_RES_LOG2_PATH = "D:/Projects/Biomio/Test1/FaceDB/parsed_data2"

def run():
    sanalyser = StatisticsAnalyser(ImageErrorFormat(), ImageErrorCollector())
    sanalyser.parse(PARSED_LOG_PATH, ERROR_LOG_PATH, DATA_FILES_PATH)

    # resultanalyser = StatisticsAnalyser(VerificationResultFormat(), VerificationCollector())
    # resultanalyser.parse(PARSED_RES_LOG_PATH, STAT_LOG_PATH, DATA_FILES_PATH)
    resultanalyser = StatisticsAnalyser(VerificationResultFormat(), VerificationCollector())
    resultanalyser.parse(PARSED_RES_LOG2_PATH, STAT_LOG2_PATH, DATA_FILES2_PATH)

if __name__ == '__main__':
    run()
