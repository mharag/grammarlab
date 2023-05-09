import logging
from inspect import getmro
from typing import Callable, Union

log = logging.getLogger("grammarlab.Grammar")


def formatter(event_type):
    class Wrapper:
        def __init__(self, func):
            self.func = func

        def __set_name__(self, owner, name):
            owner.register_formatter(object_type=event_type, function=self.func)
            setattr(owner, name, self.func)

    return Wrapper


class Export:
    """Base class for exporters

    This class is used to export objects to various output formats.
    Every exporter has some formatters registered to it.
    Formatters are functions that take object and return string representation
    of this object in some format.
    Formatters are registered using :func:`formatter` decorator.
    Formatter handles one object type and all its subclasses.

    When exporter is asked to export object,
    it tries to find formatter for this object class. If it fails, it tries to find
    formatter for every class in object's mro. If it fails again, it raises ValueError.

    """
    @classmethod
    def register_formatter(cls, object_type: Union[object, str], function: Callable):
        """Register formatter for object type

        This method shuld not be called directly. Use :func:`formatter` decorator instead.
        Only one formatter can be registered for one object type.

        Args:
            object_type: class or string representing class name
            function: formatter function

        """
        if not hasattr(cls, "_exporters"):
            cls._exporters = {}
        if object_type in cls._exporters:
            log.error(
                "Formatter for object %s already registered.", object_type
            )
        cls._exporters[object_type] = function

    def export(self, obj, *args, **kwargs):
        """Export object to string

        Exporters try to find formatter for object class.
        It starts with most specific class and goes up in mro.

        Args:
            obj: object to export
            *args: additional arguments
            **kwargs: additional keyword arguments

        Keep in mind that additional arguments must be supported by formatter for obj
        and are discouraged in most cases.

        """
        if obj is None:
            return ""
        for cls in getmro(obj.__class__):
            if cls in self._exporters:
                return self._exporters[cls](self, obj, *args, **kwargs)
            if cls.__name__ in self._exporters:
                return self._exporters[cls.__name__](self, obj, *args, **kwargs)
        raise ValueError(f"Cannot export object {obj} of type {obj.__class__}")
