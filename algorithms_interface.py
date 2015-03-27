__author__ = 'vitalius.parubochyi'

from algo_module.imgobj import loadImageObject
from algo_module.recognition import (getClustersMatchingDetectorWithoutTemplate,
                                     getClustersMatchingDetectorWithL0Template,
                                     getClustersMatchingDetectorWithL1Template)


class AlgorithmsInterface:
    def __init__(self):
        pass

    @staticmethod
    def getAlgorithm(algoID):
        """

        :param algoID: Unique algorithm identificator
                001     - Verification algorithms
                001001  - Clustering Matching Verification algorithm
                            without creating template
                001002  - Clustering Matching Verification algorithm
                            with creating L0-layer template
                001003  - Clustering Matching Verification algorithm
                            with creating L0-layer template
                002     - Identification algorithms
        :return: Algorithm Object instance
        """
        if algoID and len(algoID) == 6:
            algorithms = {"001001": getClustersMatchingDetectorWithoutTemplate(),
                          "001002": getClustersMatchingDetectorWithL0Template(),
                          "001003": getClustersMatchingDetectorWithL1Template()}
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
        if not algorithm:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'algoID'
            details['message'] = "Such algorithm ID %s doesn't exist." % kwargs['algoID']
            record['details'] = details
            return record
        if not kwargs.get('database', None):
            record['status'] = "data_request"
            record['algoID'] = kwargs['algoID']
            record['userID'] = kwargs['userID']
            return record
        imgobj = loadImageObject(kwargs['data'])
        if not imgobj:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'data'
            details['message'] = "Such data %s doesn't exists." % kwargs['data']
            record['details'] = details
            return record

        return record