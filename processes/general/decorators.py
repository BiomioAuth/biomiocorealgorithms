from ...logger import logger


def handler_header(fn):
    def wrapped(self, result):
        logger.debug("+++++++++++++++++++++++++++++++++++")
        logger.debug("%s::%s", fn.__class__.__name__, fn.__name__.capitalize())
        logger.debug(result)
        logger.debug("+++++++++++++++++++++++++++++++++++")
        return fn(self, result)
    return wrapped


def job_header(fn):
    def wrapped(**kwargs):
        logger.debug("-----------------------------------")
        logger.debug("%s::%s", fn.__class__.__name__, fn.__name__.capitalize())
        logger.debug(kwargs)
        logger.debug("-----------------------------------")
        return fn(**kwargs)
    return wrapped


def process_header(fn):
    def wrapped(**kwargs):
        logger.debug("===================================")
        logger.debug("%s::%s", fn.__class__.__name__, fn.__name__.capitalize())
        logger.debug(kwargs)
        logger.debug("===================================")
        return fn(**kwargs)
    return wrapped
