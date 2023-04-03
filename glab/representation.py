class Representable:
    """Interface for inspecting objects on different level of detial

    This interface enabled users to inspect objects implementing it on different level of detail.
    """

    def __repr__(self):
        """Detailed description of object"""
        return f"{self.__class__.__name__}()"

    def __str__(self):
        """Easy and quick to read description"""
        return repr(self)

    def serialize(self):
        """Serialization into compact definition"""
        raise NotImplementedError(f"{self.__class__.__name__} does not support serialization!")

    def deserialize(self, str_representation):
        """Deserialization from compact definition"""
        raise NotImplementedError(f"{self.__class__.__name__} does not support serialization!")

    def cli_output(self):
        """Formation for command-line """
        return str(self)
