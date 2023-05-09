from grammarlab.core.common import NonTerminal, Terminal
from grammarlab.grammars import CF
from grammarlab.transformations.chomsky_normal_form import (
    find_generating_symbols,
    find_nullable_symbols,
    find_reachable_symbols,
    find_unit_pairs,
    remove_epsilon_rules,
    remove_unit_rules,
    remove_useless_symbols,
    transform_to_chomsky,
)

P = [
    ("S", "aAB"),
    ("A", "a"),
    ("B", "b"),
    ("A", ""),
    ("B", ""),
    ("X", "X"),
]
grammar = CF({"S", "A", "B", "X"}, {"a", "b"}, P, "S")

P = [
    ("S", "A"),
    ("A", "B"),
    ("A", "a"),
    ("B", "b"),
    ("X", "X"),
]
grammar1 = CF({"S", "A", "B", "X"}, {"a", "b"}, P, "S")

S, A, B, X = NonTerminal("S"), NonTerminal("A"), NonTerminal("B"), NonTerminal("X")
a, b = Terminal("a"), Terminal("b")


def test_find_generating_symbols():
    assert find_generating_symbols(grammar) == {A, B, S, a, b}


def test_find_reachable_symbols():
    assert find_reachable_symbols(grammar) == {A, B, S, a, b}


def test_find_nullable_symbols():
    assert find_nullable_symbols(grammar) == {A, B}


def test_remove_epsilon_rules():
    new_grammar = remove_epsilon_rules(grammar)
    assert all(len(rule.rhs) != 0 for rule in new_grammar.rules)
    assert len([configuration.sential_form for configuration in new_grammar.derive(10)]) == 4


def test_find_unit_rules():
    assert find_unit_pairs(grammar1) == {(S, S), (A, A), (B, B), (S, A), (A, B), (S, B), (X, X)}


def test_remove_unit_rules():
    new_grammar = remove_unit_rules(grammar1)
    assert all((len(rule.rhs) != 1 or rule.rhs.is_sentence) for rule in new_grammar.rules)
    assert len([configuration.sential_form for configuration in new_grammar.derive(10)]) == 2


def test_remove_useless_symbols():
    new_grammar = remove_useless_symbols(grammar1)
    assert len(new_grammar.rules) == 4


def test_chomsky():
    new_grammar = transform_to_chomsky(grammar)
    for rule in new_grammar.rules:
        assert (
            (
                len(rule.rhs) == 2
                and rule.rhs[0] in new_grammar.non_terminals
                and rule.rhs[1] in new_grammar.non_terminals
            ) or (
                len(rule.rhs) == 1
                and rule.rhs[0] in new_grammar.terminals
            )
        )
    assert {str(sentence.sential_form) for sentence in new_grammar.derive(10)} == {"a a b", "a a", "a b", "a"}
