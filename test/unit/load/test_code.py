from glab.core.alphabet import Alphabet, NonTerminal, SymbolType, Terminal
from glab.load.code import CodeLoad

a = Terminal("a")
A = NonTerminal("A")


def test_symbol():
    assert CodeLoad.symbol("a", SymbolType.TERMINAL) == a
    assert CodeLoad.symbol("A", SymbolType.NON_TERMINAL) == A


def test_alphabet():
    assert CodeLoad.alphabet({"a"}, SymbolType.TERMINAL) == Alphabet({a})
    assert CodeLoad.alphabet({"A"}, SymbolType.NON_TERMINAL) == Alphabet({A})


def test_string():
    assert CodeLoad.string("aa", Alphabet({a})) == a + a
    assert CodeLoad.string("A A", Alphabet({A}), delimiter=" ") == A + A


def test_phrase_rule():
    assert CodeLoad.phrase_rule("AA", "aa", Alphabet({a, A})).lhs == A + A
    assert CodeLoad.phrase_rule(["A", "A"], ["a", "a"], Alphabet({a, A})).rhs == a + a


def test_phrase_grammar():
    grammar = CodeLoad.phrase_grammar({"A"}, {"a"}, [("AA", "aa")], "A")
    assert grammar.non_terminals == Alphabet({A})
    assert grammar.terminals == Alphabet({a})
    assert grammar.rules[0].lhs == A + A
    assert grammar.start_symbol == A
