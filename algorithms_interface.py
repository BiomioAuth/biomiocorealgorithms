__author__ = 'vitalius.parubochyi'

from algorithms.imgobj import loadImageObject
from algorithms.recognition import (getClustersMatchingDetectorWithoutTemplate,
                                    getClustersMatchingDetectorWithL0Template,
                                    getClustersMatchingDetectorWithL1Template,
                                    getIntersectMatchingDetector)
import logger
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
        logger.logger.debug('###################################')
        logger.logger.debug('Verification Process')
        logger.logger.debug('Starting...')
        record = dict()
        if not kwargs:
            record['status'] = "error"
            record['type'] = "Algorithm settings are empty"
            logger.logger.debug('Error::%s' % record['type'])
            return record
        if not kwargs.get('userID', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'userID'
            details['message'] = "The user ID is empty."
            record['details'] = details
            logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
            return record
        logger.logger.debug('User ID: %s' % kwargs['userID'])
        if not kwargs.get('algoID', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'algoID'
            details['message'] = "The algorithm ID is empty."
            record['details'] = details
            logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
            return record
        logger.logger.debug('Algorithm ID: %s' % kwargs['algoID'])
        algorithm = AlgorithmsInterface.getAlgorithm(kwargs['algoID'])
        if not algorithm:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'algoID'
            details['message'] = "Such algorithm ID %s doesn't exist." % kwargs['algoID']
            record['details'] = details
            logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
            return record
        if not kwargs.get('data', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'data'
            details['message'] = "The data source is empty."
            record['details'] = details
            logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
            return record
        if not algorithm.importSettings(AlgorithmsInterface.loadSettings(kwargs['algoID'])):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['message'] = "Cannot loading settings."
            record['details'] = details
            logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
            return record
        if not kwargs.get('action', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'action'
            details['message'] = "The action parameter is empty."
            record['details'] = details
            logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
            return record
        if kwargs['action'] == 'education':
            if kwargs.get('database', None):
                algorithm.importSources(kwargs['database'])
            for image_path in kwargs['data']:
                imgobj = loadImageObject(image_path)
                if not imgobj:
                    record['status'] = "error"
                    record['type'] = "Invalid algorithm settings"
                    details = dict()
                    details['param'] = 'data'
                    details['message'] = "Such data %s doesn't exists." % kwargs['data']
                    record['details'] = details
                    logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
                    return record
                algorithm.addSource(imgobj)
            sources = algorithm.exportSources()
            record['status'] = "update"
            record['algoID'] = kwargs['algoID']
            record['userID'] = kwargs['userID']
            record['database'] = sources
            logger.logger.debug('Status::The database updated.')
            return record
        elif kwargs['action'] == 'verification':
            if not kwargs.get('database', None):
                record['status'] = "data_request"
                record['algoID'] = kwargs['algoID']
                record['userID'] = kwargs['userID']
                logger.logger.debug('Status::The request of the database.')
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
                logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
                return record
            result = algorithm.verify(imgobj)
            record['status'] = "result"
            record['result'] = result > algorithm.kodsettings.probability
            record['userID'] = kwargs['userID']
            logger.logger.debug('Result::%s' % str(record['result']))
            return record
        else:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'action'
            details['message'] = "Such action %s doesn't exists." % kwargs['action']
            record['details'] = details
            logger.logger.debug('Error::%s::%s' % record['type'], details['message'])
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