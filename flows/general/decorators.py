from ...logger import logger


def _get_options(data):
    options = {}
    if data is not None:
        options = data.get('options', {})
    return options


def algorithm_header(fn):
    def wrapped(self, data):
        options = _get_options(data)
        logger.debug("===================================")
        logger.debug("{}::{}".format(self.__class__.__name__, fn.__name__))
        if options.get('print_data', False):
            logger.debug(data)
        logger.debug("===================================")
        return fn(self, data)
    return wrapped
