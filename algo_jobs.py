import shutil
import tempfile
from biomio.constants import REDIS_PROBE_RESULT_KEY
from biomio.protocol.storage.redis_storage import RedisStorage
from algorithms_interface import AlgorithmsInterface
import logging
import os
import binascii
import json

logger = logging.getLogger(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALGO_DB_PATH = os.path.join(APP_ROOT, 'data')


def verification_job(callback_code, data, fingerprint):
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
    result = True
    settings = dict()
    settings['algoID'] = "001002"
    settings['userID'] = "0000000000000"
    settings['database'] = load_sources(os.path.join(ALGO_DB_PATH, "%s.json" % fingerprint))
    logger.info('Running verification for user - %s, with given parameters - %s' % (settings['userID'], settings))
    for sample in data:
        if result:
            break
        try:
            temp_image_path = tempfile.mkdtemp(dir=APP_ROOT)
            fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
            os.close(fd)
            photo_data = binascii.a2b_base64(str(sample))
            with open(temp_image, 'wb') as f:
                f.write(photo_data)
            settings['data'] = temp_image
            record = AlgorithmsInterface.verification(**settings)
            if record['status'] == "result":
                # record = dictionary:
                #      key          value
                #      'status'     "result"
                #      'result'     bool value: True is verification successfully, otherwise False
                #      'userID'     Unique user identificator
                #
                # Need save to redis
                result = record.get('result', False)
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
                print record['status'], record['type'], record['details']
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
        except Exception as e:
            logger.exception(e)
        finally:
            shutil.rmtree(temp_image_path)
    RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)
    logger.info('Verification was run for user - %s, with given parameters - %s' % (settings['userID'], settings))
    # try:
    #     record = AlgorithmsInterface.verification(**kwargs)
    #     if record['status'] == "result":
    #         # record = dictionary:
    #         #      key          value
    #         #      'status'     "result"
    #         #      'result'     bool value: True is verification successfully, otherwise False
    #         #      'userID'     Unique user identificator
    #         #
    #         # Need save to redis
    #         result = record.get('result', False)
    #         RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)
    #         pass
    #     elif record['status'] == "data_request":
    #         # record = dictionary:
    #         #      key          value
    #         #      'status'     "data_request"
    #         #      'userID'     Unique user identificator
    #         #      'algoID'     Unique algorithm identificator
    #         #
    #         # Need save to redis as data request (for this we can use this dictionary)
    #         pass
    #     elif record['status'] == "update":
    #         # record = dictionary:
    #         #      key          value
    #         #      'status'     "update"
    #         #      'userID'     Unique user identificator
    #         #      'algoID'     Unique algorithm identificator
    #         #      'database'   BLOB data of user, with userID, for verification algorithm algoID
    #         #
    #         # Need update record in algorithms database or create record for user userID and algorithm
    #         # algoID if it doesn't exists
    #         pass
    #     elif record['status'] == "error":
    #         print record['status'], record['type'], record['details']
    #         # record = dictionary:
    #         #      key          value
    #         #      'status'     "error"
    #         #      'type'       Type of error
    #         #      'userID'     Unique user identificator
    #         #      'algoID'     Unique algorithm identificator
    #         #      'details'    Error details dictionary
    #         #
    #         # Algorithm can have three types of errors:
    #         #       "Algorithm settings are empty"
    #         #        in this case fields 'userID', 'algoID', 'details' are empty
    #         #       "Invalid algorithm settings"
    #         #        in this case 'details' dictionary has following structure:
    #         #               key         value
    #         #               'params'    Parameters key ('data')
    #         #               'message'   Error message (for example "File <path> doesn't exists")
    #         #       "Internal algorithm error"
    #         # Need save to redis
    #         pass
    #     logger.info('Verification was run for user - %s, with given parameters - %s' % (kwargs['userID'], kwargs))
    # except Exception as e:
    #     logger.exception(msg=str(e))
    #
    # return result


def load_sources(path):
    if len(path):
        if not os.path.exists(path):
            return dict()
        with open(path, "r") as data_file:
            source = json.load(data_file)
            return source
    return dict()