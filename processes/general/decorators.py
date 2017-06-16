from ....protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from ....constants import REDIS_DO_NOT_STORE_RESULT_KEY
from ..helpers import partial_results_handler
from handling import remove_temp_data
from ...logger import logger


def _get_options(data):
    options = {}
    if data is not None:
        options = data.get('options', {})
    return options


def handler_header(fn):
    def wrapped(self, result):
        options = _get_options(result)
        logger.debug("+++++++++++++++++++++++++++++++++++")
        logger.debug("%s::%s", self.__class__.__name__, fn.__name__.capitalize())
        if options.get('print_data', False):
            logger.debug(result)
        logger.debug("+++++++++++++++++++++++++++++++++++")
        return fn(self, result)
    return wrapped


def job_header(fn):
    def wrapped(cls, callback_code, **kwargs):
        options = _get_options(kwargs)
        logger.debug("-----------------------------------")
        logger.debug("%s::%s", cls.__name__, fn.__name__.capitalize())
        if options.get('print_data', False):
            logger.debug(kwargs)
        logger.debug("-----------------------------------")
        return fn(cls, callback_code, **kwargs)
    return wrapped


def process_header(fn):
    def wrapped(cls, **kwargs):
        options = _get_options(kwargs)
        logger.debug("===================================")
        logger.debug("%s::%s", cls.__name__, fn.__name__.capitalize())
        if options.get('print_data', False):
            logger.debug(kwargs)
        logger.debug("===================================")
        return fn(cls, **kwargs)
    return wrapped


def store_job_result(fn):
    def wrapped(cls, callback_code, **kwargs):
        res = fn(cls, callback_code, **kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=res, callback_code=callback_code)
        return None
    return wrapped


def store_partial_result(fn):
    def wrapped(cls, callback_code, **kwargs):
        record = fn(cls, callback_code, **kwargs)
        if partial_results_handler(callback_code, record) and 'data_file' in kwargs:
            remove_temp_data(kwargs['data_file'])
        return None
    return wrapped
