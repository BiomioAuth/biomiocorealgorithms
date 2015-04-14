from __future__ import absolute_import
from rq import Queue, use_connection
from redis import Redis
from logger import worker_logger

use_connection()
q = Queue(connection=Redis())


def run_algo_job(job_to_run, **kwargs):
    """
        Put job in worker's queue.
    :param job_to_run:
    :param kwargs:
    """
    worker_logger.info('Running job - %s' % str(job_to_run))
    q.enqueue(job_to_run, **kwargs)
