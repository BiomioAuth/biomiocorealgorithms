from biomio.constants import REST_REGISTER_BIOMETRICS, TRAINING_DATA_TABLE_CLASS_NAME, get_ai_training_response
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.settings import settings as biomio_settings
from biomio.algorithms.logger import logger
from requests.exceptions import HTTPError
import requests
import tempfile
import binascii
import cPickle
import base64
import json
import os


def ai_response_sender(ai_code, ai_response_type):
    response_type = base64.b64encode(json.dumps(ai_response_type))
    register_biometrics_url = biomio_settings.ai_rest_url % (REST_REGISTER_BIOMETRICS % (ai_code, response_type))
    response = requests.post(register_biometrics_url)
    try:
        response.raise_for_status()
        logger.info('AI should now know that training change state with code - %s and response type - %s' %
                    (ai_code, response_type))
    except HTTPError as e:
        logger.exception(e)
        logger.exception('Failed to tell AI that training change state, reason - %s' % response.reason)


def tell_ai_training_results(result, ai_response_type, try_type, ai_code):
    if isinstance(result, bool) and result:
        ai_response_type.update(get_ai_training_response(try_type))
    try:
        logger.info('Telling AI that training is finished with code - %s and result - %s' %
                    (ai_code, result))
        ai_response_sender(ai_code, ai_response_type)
    except Exception as e:
        logger.error('Failed to build rest request to AI - %s' % str(e))
        logger.exception(e)


def get_algo_db(probe_id):
    database = MySQLDataStoreInterface.get_object(table_name=TRAINING_DATA_TABLE_CLASS_NAME, object_id=probe_id)
    return cPickle.loads(base64.b64decode(database.data)) if database is not None else {}


def save_images(images, temp_image_path):
    image_paths = []
    for image in images:
        fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
        os.close(fd)
        photo_data = binascii.a2b_base64(str(image))
        with open(temp_image, 'wb') as f:
            f.write(photo_data)
        image_paths.append(temp_image)
    return image_paths


def store_test_photo_helper(root_dir, image_paths):
    import tempfile
    import shutil
    import os

    TEST_PHOTO_PATH = os.path.join(root_dir, 'test_photo')
    if not os.path.exists(TEST_PHOTO_PATH):
        os.makedirs(TEST_PHOTO_PATH)

    TEST_IMAGE_FOLDER = tempfile.mkdtemp(dir=TEST_PHOTO_PATH)
    if not os.path.exists(TEST_IMAGE_FOLDER):
        os.makedirs(TEST_IMAGE_FOLDER)

    for path in image_paths:
        shutil.copyfile(path, os.path.join(TEST_IMAGE_FOLDER, os.path.basename(path)))
    return TEST_IMAGE_FOLDER
