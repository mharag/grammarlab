from functools import wraps
from logging import getLogger

logger = getLogger("glab.filter")


def grammar_filter(func: bool = None, *, show_filtered: bool = False):
    LOG = logger.info if show_filtered else logger.debug

    def decorator(func):
        @wraps(func)
        def wrapper(sential_form):
            result = func(sential_form)
            if not result:
                LOG("%s filtered %s", func.__name__, sential_form)
            return result
        return wrapper
    return decorator(func) if func else decorator
