PARALLEL_USAGE = "PARALLEL_USAGE"
SEQUENTIAL_USAGE = "SEQUENTIAL_USAGE"

CURRENT_USAGE = PARALLEL_USAGE


def is_parallel():
    return CURRENT_USAGE == PARALLEL_USAGE
