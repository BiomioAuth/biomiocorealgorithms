import shutil
import tempfile
from biomio.constants import REDIS_PROBE_RESULT_KEY, REDIS_RESULTS_COUNTER_KEY, REDIS_PARTIAL_RESULTS_KEY
from biomio.protocol.storage.redis_storage import RedisStorage
from algorithms_interface import AlgorithmsInterface
import os
import binascii
import json
from json import dumps
from logger import worker_logger


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALGO_DB_PATH = os.path.join(APP_ROOT, 'algorithms', 'data')


def load_sources(path):
    if len(path):
        if not os.path.exists(path):
            return dict()
        with open(path, "r") as data_file:
            source = json.load(data_file)
            return source
    return dict()


def verification_job(image, fingerprint, settings, callback_code, result_code):
    """
        Runs verification for user with given image
    :param image: to run verification for
    :param fingerprint: app_id
    :param settings: settings with values for algoId and userID
    :param callback_code: code of the callback which should be executed after job is finished.
    :param result_code: code of the result in case we are running job in parallel.
    """
    worker_logger.info('Running verification for user - %s, with given parameters - %s' % (settings.get('userID'),
                                                                                           settings))
    result = False
    settings.update({'database': load_sources(os.path.join(ALGO_DB_PATH, "%s.json" % fingerprint))})
    settings.update({'action': 'verification'})
    temp_image_path = tempfile.mkdtemp(dir=APP_ROOT)
    try:
        fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
        os.close(fd)
        photo_data = binascii.a2b_base64(str(image))
        with open(temp_image, 'wb') as f:
            f.write(photo_data)
        settings.update({'data': temp_image})
        algo_result = AlgorithmsInterface.verification(**settings)
        if algo_result.get('status', '') == "result":
            # record = dictionary:
            # key          value
            #      'status'     "result"
            #      'result'     bool value: True is verification successfully, otherwise False
            #      'userID'     Unique user identifier
            #
            # Need save to redis
            result = algo_result.get('result', False)
        elif algo_result.get('status', '') == "data_request":
            # record = dictionary:
            # key          value
            #      'status'     "data_request"
            #      'userID'     Unique user identifier
            #      'algoID'     Unique algorithm identifier
            #
            # Need save to redis as data request (for this we can use this dictionary)
            pass
        elif algo_result.get('status', '') == "error":
            worker_logger.exception('Error during verification - %s, %s, %s' % (algo_result.get('status'),
                                                                                algo_result.get('type'),
                                                                                algo_result.get('details')))
            # record = dictionary:
            # key          value
            #      'status'     "error"
            #      'type'       Type of error
            #      'userID'     Unique user identifier
            #      'algoID'     Unique algorithm identifier
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
        worker_logger.exception(e)
    finally:
        RedisStorage.persistence_instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                                 value=result)
        results_counter = RedisStorage.persistence_instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                                  result_code)
        if results_counter <= 0:
            gathered_results = RedisStorage.persistence_instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                                   callback_code)
            worker_logger.debug('All gathered results for verification job - %s' % gathered_results)
            true_count = float(gathered_results.count('True'))
            result = ((true_count / len(gathered_results)) * 100) >= 50
            RedisStorage.persistence_instance().delete_data(key=REDIS_RESULTS_COUNTER_KEY % result_code)
            RedisStorage.persistence_instance().delete_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
            RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)
        shutil.rmtree(temp_image_path)
    worker_logger.info('Verification finished for user - %s, with result - %s' % (settings.get('userID'), result))


def training_job(images, fingerprint, settings, callback_code):
    """
        Runs education for given user with given array of images.
    :param images: array of images to run verification on.
    :param fingerprint: current app_id
    :param settings: dictionary which contains information about algoId and userID
    :param callback_code: code of the callback that should be executed after job is finished
    """
    worker_logger.info('Running training for user - %s, with given parameters - %s' % (settings.get('userID'),
                                                                                       settings))
    result = False
    settings.update({'action': 'education'})
    temp_image_path = tempfile.mkdtemp(dir=APP_ROOT)
    try:
        image_paths = []
        for image in images:
            fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
            os.close(fd)
            photo_data = binascii.a2b_base64(str(image))
            with open(temp_image, 'wb') as f:
                f.write(photo_data)
            image_paths.append(temp_image)
        settings.update({'data': image_paths})
        algo_result = AlgorithmsInterface.verification(**settings)
        if algo_result.get('status', '') == "update":
            # record = dictionary:
            # key          value
            #      'status'     "update"
            #      'userID'     Unique user identificator
            #      'algoID'     Unique algorithm identificator
            #      'database'   BLOB data of user, with userID, for verification algorithm algoID
            #
            # Need update record in algorithms database or create record for user userID and algorithm
            # algoID if it doesn't exists
            database = algo_result.get('database', None)
            database_path = os.path.join(ALGO_DB_PATH, "%s.json" % fingerprint)
            if database is not None:
                result = True
                with open(database_path, 'wb') as f:
                    f.write(dumps(database))
        elif algo_result.get('status', '') == "error":
            worker_logger.exception('Error during education - %s, %s, %s' % (algo_result.get('status'),
                                                                             algo_result.get('type'),
                                                                             algo_result.get('details')))
            # record = dictionary:
            # key          value
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
        worker_logger.exception(e)
    finally:
        RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)
        shutil.rmtree(temp_image_path)
    worker_logger.info('training finished for user - %s, with result - %s' % (settings.get('userID'), result))