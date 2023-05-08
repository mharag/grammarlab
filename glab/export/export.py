import logging
from inspect import getmro

log = logging.getLogger("glab.Grammar")


def formatter(event_type):
    class Wrapper:
        def __init__(self, func):
            self.func = func

        def __set_name__(self, owner, name):
            owner.register_formatter(object_type=event_type, function=self.func)
            setattr(owner, name, self.func)

    return Wrapper


class Export:
    @classmethod
    def register_formatter(cls, object_type, function):
        if not hasattr(cls, "exporters"):
            cls.exporters = {}
        if object_type in cls.exporters:
            log.error(
                "Formatter for object %s already registered.", object_type
            )
        cls.exporters[object_type] = function

    def export(self, obj, *args, **kwargs):
        if obj is None:
            return ""
        for cls in getmro(obj.__class__):
            if cls in self.exporters:
                return self.exporters[cls](self, obj, *args, **kwargs)
            if cls.__name__ in self.exporters:
                return self.exporters[cls.__name__](self, obj, *args, **kwargs)
        raise ValueError(f"Cannot export object {obj} of type {obj.__class__}")
