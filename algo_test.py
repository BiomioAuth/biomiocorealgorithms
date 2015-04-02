__author__ = 'vitalius.parubochyi'


from algorithms_interface import AlgorithmsInterface
import json
import os


def main():
    error_algoID()
    error_database()
    error_data()
    # success()
    education()


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
    settings['data'] = "D:/Projects/Biomio/Test1/yaleB11_P00A+000E+00.png"
    print AlgorithmsInterface.verification(**settings)


def error_data():
    settings = dict()
    settings['action'] = 'verification'
    settings['algoID'] = "001002"
    settings['userID'] = "0000000000000"
    settings['database'] = loadSources("D:/Projects/Biomio/Test1/source4/data.json")
    print AlgorithmsInterface.verification(**settings)


def success():
    settings = dict()
    settings['action'] = 'verification'
    settings['algoID'] = "001003"
    settings['userID'] = "0000000000000"
    settings['data'] = "D:/Projects/Biomio/Test1/db/yaleB11/yaleB11_P00A+000E+00.pgm"
    settings['database'] = loadSources("D:/Projects/Biomio/Test1/source/data" + settings['algoID'] + ".json")
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