import logging
# from gui_logger import QtHandler

import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALGO_LOGS_PATH = os.path.join(APP_ROOT, 'algorithms', 'logs')

logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sys_logger = logging.getLogger("algorithms.full")
sys_logger.setLevel(logging.DEBUG)

# handler = QtHandler()
# handler.setFormatter(logging.Formatter("%(levelname)-1s" + '\t' + " [%(asctime)s]" + '\t' + " %(message)s"))
# logger.addHandler(handler)
# sys_logger.addHandler(handler)

file_handler = logging.FileHandler(ALGO_LOGS_PATH + "basic_log.txt")
file_handler.setFormatter(logging.Formatter("%(levelname)-1s" + '\t' + " [%(asctime)s]" + '\t' + " %(message)s"))
logger.addHandler(file_handler)

ext_handler = logging.FileHandler(ALGO_LOGS_PATH + "ext_log.txt")
ext_handler.setFormatter(logging.Formatter("%(levelname)-1s" + '\t' + " [%(asctime)s]" + '\t' + " %(message)s"))
logger.addHandler(ext_handler)
sys_logger.addHandler(ext_handler)