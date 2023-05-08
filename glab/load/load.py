import logging
from functools import partial
from inspect import getmro

log = logging.getLogger("glab.Grammar")


def loader(event_type):
    """Decorator for registering loaders to Importer

    Args:
        event_type: class or string representing class name

    """
    class Wrapper:
        def __init__(self, func):
            self.func = func

        def __set_name__(self, owner, name):
            owner.register_loader(object_type=event_type, function=self.func)
            setattr(owner, name, self.func)

    return Wrapper


class Load:
    """Base class for loaders

    This class is used to load objects from various input formats.
    Every Importer has some loaders registered to it.
    Loaders are functions that take some input and return object.
    Loaders are registered using :func:`loader` decorator.
    Loader handles one object type and all its subclasses.

    When importer is asked to load object from some input,
    it tries to find loader for this object class. If it fails, it tries to find
    loader for every class in object's mro. If it fails again, it raises ValueError.

    """
    @classmethod
    def register_loader(cls, object_type, function):
        """Register loader for object type

        This method shuld not be called directly. Use :func:`loader`
        decorator instead. Only one loader can be registered for one object type.

        Args:
            object_type: class or string representing class name
            function: loader function

        """
        if not hasattr(cls, "loaders"):
            cls.loaders = {}
        if object_type in cls.loaders:
            log.error(
                "Loader for class %s already registered.", object_type
            )
        cls.loaders[object_type] = function

    def get_loader(self, target_cls):
        """Get loader for class

        Args:
            target_cls: class to load

        Returns:
            loader function with mapped cls argument

        Function returned by this method can be directly called with input
        as argument. Target class doesn't have to be specified.

        """
        for cls in getmro(target_cls):
            if cls in self.loaders:
                return partial(self.loaders[cls], self, target_cls)
            if cls.__name__ in self.loaders:
                return partial(self.loaders[cls.__name__], self, target_cls)
        raise ValueError(f"Cannot find loader for class {target_cls}.")

    def load(self, target_cls, *args, **kwargs):
        """Load object from input

        Args:
            target_cls: class to load
            *args: arguments passed to loader
            **kwargs: keyword arguments passed to loader

        Returns:
            loaded object

        """
        return self.get_loader(target_cls)(*args, **kwargs)
