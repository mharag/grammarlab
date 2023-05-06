from glab.core.alphabet import SymbolType, Terminal
from glab.core.extended_symbol import ExtendedSymbol


class Symbol1(ExtendedSymbol):
    variants = {
        "variant1": (SymbolType.NON_TERMINAL, "1"),
        "variant2": (SymbolType.NON_TERMINAL, "2"),
    }


class Symbol2(ExtendedSymbol):
    variants = {
        "variant1": (SymbolType.NON_TERMINAL, "1"),
        "variant2": (SymbolType.NON_TERMINAL, "2"),
    }


def test_singleton():
    s1 = Symbol1(Terminal("S"))
    s2 = Symbol1(Terminal("S"))
    s3 = Symbol1(Terminal("X"))
    s4 = Symbol2(Terminal("S"))

    assert id(s1) == id(s2)
    assert id(s1) != id(s3)
    assert id(s2.variant1) != id(s1.variant2)
    assert id(s2.variant1) == id(s1.variant1)
    assert id(s1) != id(s4)


def test_variants():
    s1 = Symbol1(Terminal("S"))
    assert s1.type == SymbolType.TERMINAL
    assert s1.id == "S"
    assert s1.variant1.id == "S_1"
    assert s1.variant2.id == "S_2"
    assert s1.variant1.variant2.id == "S_2"
    assert s1.variant1.type == SymbolType.NON_TERMINAL
    assert s1.variant1.base == s1
