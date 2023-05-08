from functools import wraps
from logging import getLogger
from typing import Optional

logger = getLogger("glab.filter")


def grammar_filter(func: Optional[callable] = None, *, show_filtered: bool = False):
    """Decorator for grammar filter.

    Function will be evaluated for each configuration.
    If function returns False, configuration will be filtered out.

    Args:
        func: Filter function. Defaults to None.
        show_filtered: Show filtered configurations. Defaults to False.

    Returns:
        Decorator if func is None else decorated function.

    Examples:
        >>> @grammar_filter
        ... def filter_func(configuration):
        ...     return len(configuration.sential_form) < 10
        ...
        >>> grammar.set_filter(filter_func)
    """
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
