__author__ = 'vitalius.parubochyi'

from algorithms_interface import AlgorithmsInterface
import logging


logger = logging.getLogger(__name__)


def verification_job(**kwargs):
    """
    Creating verification job

    :param kwargs: dictionary:
            key         value
            'action'    Action name
            'userID'    Unique user identificator
            'algoID'    Unique algorithm identificator (for verification algorithms algoID="001xxx", where
                        001 - key of verification algorithms type and xxx - number of algorithm realization)
            'data'      Absolute path to image for verification
            'database'  BLOB data of user, with userID, for verification algorithm algoID

        if kwargs['action'] == 'education' use following settings:
            'userID'    Unique user identificator
            'algoID'    Unique algorithm identificator
            'data'      List of paths to images for education
            'database'  BLOB data of user, with userID, for verification algorithm algoID

        if kwargs['action'] == 'verification' use following settings:
            'userID'    Unique user identificator
            'algoID'    Unique algorithm identificator
            'data'      Absolute path to image for verification
            'database'  BLOB data of user, with userID, for verification algorithm algoID
    """
    logger.info('Running verification for user - %s, with given parameters - %s' % (kwargs['userID'], kwargs))
    try:
        record = AlgorithmsInterface.verification(kwargs)
        if record['status'] == "result":
            # record = dictionary:
            #      key          value
            #      'status'     "result"
            #      'result'     bool value: True is verification successfully, otherwise False
            #      'userID'     Unique user identificator
            #
            # Need save to redis
            pass
        elif record['status'] == "data_request":
            # record = dictionary:
            #      key          value
            #      'status'     "data_request"
            #      'userID'     Unique user identificator
            #      'algoID'     Unique algorithm identificator
            #
            # Need save to redis as data request (for this we can use this dictionary)
            pass
        elif record['status'] == "update":
            # record = dictionary:
            #      key          value
            #      'status'     "update"
            #      'userID'     Unique user identificator
            #      'algoID'     Unique algorithm identificator
            #      'database'   BLOB data of user, with userID, for verification algorithm algoID
            #
            # Need update record in algorithms database or create record for user userID and algorithm
            # algoID if it doesn't exists
            pass
        elif record['status'] == "error":
            # record = dictionary:
            #      key          value
            #      'status'     "error"
            #      'type'       Type of error
            #      'userID'     Unique user identificator
            #      'algoID'     Unique algorithm identificator
            #      'details'    Error details dictionary
            #
            # Algorithm can have three types of errors:
            #       "Algorithm settings are empty"
            #        in this case fields 'userID', 'algoID', 'details' are empty
            #       "Invalid algorithm settings"
            #        in this case 'details' dictionary has following structure:
            #               key         value
            #               'params'    Parameters key ('data')
            #               'message'   Error message (for example "File <path> doesn't exists")
            #       "Internal algorithm error"
            # Need save to redis
            pass
        logger.info('Verification was run for user - %s, with given parameters - %s' % (kwargs['userID'], kwargs))
    except Exception as e:
        logger.exception(msg=str(e))