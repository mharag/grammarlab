from glab.checkers import (chomsky_normal_form, greibach_normal_form,
                           kuruda_normal_form_type_0)
from glab.grammars import CF, RE


def test_chomsky_normal_form():
    grammar = CF({"S"}, {"a"}, [("S", "aa"), ("S", "Saa")], "S")
    assert not chomsky_normal_form(grammar)

    grammar = CF({"S"}, {"a"}, [("S", "a"), ("S", "SS")], "S")
    assert chomsky_normal_form(grammar)


def test_kuruda_normal_form_type_0():
    grammar = RE({"S"}, {"a"}, [("S", "aa")], "S")
    assert not kuruda_normal_form_type_0(grammar)

    grammar = RE({"S"}, {"a"}, [("SS", "SS"), ("S", "SS"), ("S", [None])], "S")
    assert kuruda_normal_form_type_0(grammar)


def test_greibach_normal_form():
    grammar = CF({"S", "X"}, {"a"}, [("S", "X")], "S")
    assert not greibach_normal_form(grammar)

    grammar = CF({"S"}, {"a"}, [("S", "a"), ("S", "aSSSSSSSS")], "S")
    assert greibach_normal_form(grammar)
