__author__ = 'vitalius.parubochyi'

from algorithms.imgobj import loadImageObject
from algorithms.recognition import (getClustersMatchingDetectorWithoutTemplate,
                                    getClustersMatchingDetectorWithL0Template,
                                    getClustersMatchingDetectorWithL1Template,
                                    getIntersectMatchingDetector)
import json
import os

SETTINGS_DIR = "D:/Projects/Biomio/Test1/source/"
# SETTINGS_DIR = "/home/alexchmykhalo/ios_screens/algorithms/"


class AlgorithmsInterface:
    def __init__(self):
        pass

    @staticmethod
    def getAlgorithm(algoID):
        """
        Return algorithm object by algorithm ID algoID.

        :param algoID: Unique algorithm identificator
                001     - Verification algorithms
                001001  - Clustering Matching Verification algorithm
                            without creating template
                001002  - Clustering Matching Verification algorithm
                            with creating L0-layer template
                001003  - Clustering Matching Verification algorithm
                            with creating L1-layer template
                001004  - Intersection Matching Verification algorithm
                002     - Identification algorithms
        :return: Algorithm object instance
        """
        if algoID and len(algoID) == 6:
            algorithms = {"001001": getClustersMatchingDetectorWithoutTemplate,
                          "001002": getClustersMatchingDetectorWithL0Template,
                          "001003": getClustersMatchingDetectorWithL1Template,
                          "001004": getIntersectMatchingDetector}
            if algorithms.keys().__contains__(algoID):
                return algorithms[algoID]()
        return None

    @staticmethod
    def verification(**kwargs):
        record = dict()
        if not kwargs:
            record['status'] = "error"
            record['type'] = "Algorithm settings are empty"
            return record
        algorithm = AlgorithmsInterface.getAlgorithm(kwargs['algoID'])
        print algorithm
        if not algorithm:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'algoID'
            details['message'] = "Such algorithm ID %s doesn't exist." % kwargs['algoID']
            record['details'] = details
            return record
        if not kwargs.get('data', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'data'
            details['message'] = "The data source is empty."
            record['details'] = details
            return record
        if not kwargs.get('database', None):
            record['status'] = "data_request"
            record['algoID'] = kwargs['algoID']
            record['userID'] = kwargs['userID']
            return record
        if not algorithm.importSettings(AlgorithmsInterface.loadSettings(kwargs['algoID'])):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['message'] = "Cannot loading settings."
            record['details'] = details
            return record
        algorithm.importSources(kwargs['database'])
        imgobj = loadImageObject(kwargs['data'])
        if not imgobj:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'data'
            details['message'] = "Such data %s doesn't exists." % kwargs['data']
            record['details'] = details
            return record
        result = algorithm.verify(imgobj)
        record['status'] = "result"
        record['result'] = result
        record['userID'] = kwargs['userID']
        return record

    @staticmethod
    def loadSettings(algoID):
        settings_path = os.path.join(SETTINGS_DIR, "info" + algoID + ".json")
        if not os.path.exists(settings_path):
            return dict()
        with open(settings_path, "r") as data_file:
            source = json.load(data_file)
            return source
        return dict()