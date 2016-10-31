from __future__ import absolute_import
from . import is_parallel

if is_parallel():
    from logger import algo_logger as logger
else:
    from logger import logger
