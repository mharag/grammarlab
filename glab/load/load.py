import logging
from functools import partial
from inspect import getmro

log = logging.getLogger("glab.GrammarBase")


def loader(event_type):
    class Wrapper:
        def __init__(self, func):
            self.func = func

        def __set_name__(self, owner, name):
            owner.register_loader(object_type=event_type, function=self.func)
            setattr(owner, name, self.func)

    return Wrapper


class Load:
    @classmethod
    def register_loader(cls, object_type, function):
        if not hasattr(cls, "loaders"):
            cls.loaders = {}
        if object_type in cls.loaders:
            log.error(
                "Loader for class %s already registered.", object_type
            )
        cls.loaders[object_type] = function

    def get_loader(self, target_cls):
        for cls in getmro(target_cls):
            if cls in self.loaders:
                return partial(self.loaders[cls], self, target_cls)
            if cls.__name__ in self.loaders:
                return partial(self.loaders[cls.__name__], self, target_cls)
        raise ValueError(f"Cannot find loader for class {target_cls}.")

    def load(self, target_cls, *args, **kwargs):
        return self.get_loader(target_cls)(*args, **kwargs)
