from time import perf_counter

from loguru import logger


def timeit(func):
    def timed(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        logger.info("{} took {:.2f} seconds".format(func.__name__, end - start))
        return result

    return timed
