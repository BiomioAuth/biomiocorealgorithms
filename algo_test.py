from algorithms_interface import AlgorithmsInterface
import json
import os

PICTURE_PATH_BAD_1 = "D:/Projects/Biomio/Test1/yaleB11_P00A+000E+00.png"
DATA_PATH_BAD_2 = "D:/Projects/Biomio/Test1/source4/data.json"
PICTURE_PATH_GOOD_3 = "D:/Projects/Biomio/Test1/db/yaleB11/yaleB11_P00A+000E+00.pgm"
FOLDER_DB_PATH_GOOD_3 = "D:/Projects/Biomio/Test1/source"

# PICTURE_PATH_BAD_1 = "/home/alexchmykhalo/ios_screens/algorithms/yaleB11_P00A+000E+00.png"
# DATA_PATH_BAD_2 = "/home/alexchmykhalo/ios_screens/algorithms/data.json"
# PICTURE_PATH_GOOD_3 = "/home/alexchmykhalo/ios_screens/algorithms/yaleB11_P00A+000E+00.pgm"
# FOLDER_DB_PATH_GOOD_3 = "/home/alexchmykhalo/ios_screens/algorithms"


def main():
    # error_algoID()
    # error_database()
    # error_data()
    success()
    # education()


def error_algoID():
    settings = dict()
    settings['action'] = 'verification'
    settings['algoID'] = "001000"
    settings['userID'] = "0000000000000"
    print AlgorithmsInterface.verification(**settings)


def error_database():
    settings = dict()
    settings['action'] = 'verification'
    settings['algoID'] = "001001"
    settings['userID'] = "0000000000000"
    settings['data'] = PICTURE_PATH_BAD_1
    print AlgorithmsInterface.verification(**settings)


def error_data():
    settings = dict()
    settings['action'] = 'verification'
    settings['algoID'] = "001002"
    settings['userID'] = "0000000000000"
    settings['database'] = loadSources(DATA_PATH_BAD_2)
    print AlgorithmsInterface.verification(**settings)


def success():
    settings = dict()
    settings['action'] = 'verification'
    settings['algoID'] = "001002"
    settings['userID'] = "0000000000000"
    settings['data'] = PICTURE_PATH_GOOD_3
    settings['database'] = loadSources(FOLDER_DB_PATH_GOOD_3 + "/data" + settings['algoID'] + ".json")
    print AlgorithmsInterface.verification(**settings)


def education():
    settings = dict()
    settings['action'] = 'education'
    settings['algoID'] = "001002"
    settings['userID'] = "0000000000000"
    settings['data'] = ["D:/Projects/Biomio/Test1/db/yaleB11/yaleB11_P00A+000E+00.pgm",
                        "D:/Projects/Biomio/Test1/db/yaleB11/yaleB11_P00A+000E+20.pgm",
                        "D:/Projects/Biomio/Test1/db/yaleB11/yaleB11_P00A+000E+45.pgm"]
    print AlgorithmsInterface.verification(**settings)


def loadSources(path):
    if len(path):
        if not os.path.exists(path):
            return dict()
        with open(path, "r") as data_file:
            source = json.load(data_file)
            return source
    return dict()


if __name__ == '__main__':
    main()