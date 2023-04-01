from functools import wraps
from logging import getLogger

logger = getLogger("glab.filter")


def grammar_filter(func=None, *, show_filtered=False):
    LOG = logger.info if show_filtered else logger.debug

    def decorator(func):
        @wraps(func)
        def wrapper(sential_form):
            result = func(sential_form)
            if not result:
                LOG(f" {func.__name__} filtered {sential_form}")
            return result
        return wrapper
    return decorator(func) if func else decorator


