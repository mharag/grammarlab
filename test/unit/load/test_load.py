# pylint: disable=duplicate-code

from grammarlab.load.load import Load, loader


class A:
    pass


class B(A):
    pass


class C(A):
    pass


class LoadTest(Load):
    @loader(A)
    def loader_A(self, cls):
        return cls.__name__

    @loader("B")
    def loader_B(self, cls):  # pylint: disable=unused-argument
        return "BB"


def test_get_loader():
    assert LoadTest().get_loader(A)() == "A"
    assert LoadTest().get_loader(B)() == "BB"
    assert LoadTest().get_loader(C)() == "C"


def test_load():
    assert LoadTest().load(A) == "A"
    assert LoadTest().load(B) == "BB"
    assert LoadTest().load(C) == "C"
