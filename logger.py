import logging
# from gui_logger import QtHandler

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG
)
# handler = QtHandler()
# handler.setFormatter(logging.Formatter("%(levelname)-1s" + '\t' + " [%(asctime)s]" + '\t' + " %(message)s"))
# logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Logger:
    def __init__(self):
        self._isLogging = True
        self._level = 0
        self._log = []

    def useLogging(self, use):
        self._isLogging = use

    def level(self, l):
        self._level = l
        for i in range(0, l):
            self._log.append("")

    def debug(self, level, message):
        if self._isLogging:
            logger.log(message)
        if self._level > 0:
            log = self._log[level]
            if not log:
                log = ""
            log += message + "\n"
            self._log[level] = log