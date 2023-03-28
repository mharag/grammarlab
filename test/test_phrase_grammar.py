from grammar.alphabet import N, S, T
import pytest
from grammar.phrase_grammar import PhraseGrammarRule as Rule, PhraseGrammar as Grammar


@pytest.mark.parametrize(
    "string,lhs,expected",
    [
        (
            S([N("A"), N("B"), N("C")]),
            S([N("A"), N("B"), N("C")]),
            [0]
        ),
        (
            S([N("A"), N("A"), N("A")]),
            S([N("A"), N("A")]),
            [0, 1]
        ),
        (
            S([N("A"), N("A"), N("A")]),
            S([N("X")]),
            []
        )
    ]
)
def test_match(string, lhs, expected):
    rule = Rule(lhs, lhs)
    result = [i for i in rule.match(string)]
    assert result == expected


@pytest.mark.parametrize(
    "string,lhs,rhs,expected",
    [
        (
            S([N("A"), N("B"), N("C")]),
            S([N("A")]),
            S([N("X"), N("Y"), N("Z")]),
            [S([N("X"), N("Y"), N("Z"), N("B"), N("C")])],
        ),
        (
            S([N("A"), N("B"), N("C")]),
            S([N("A"), N("B")]),
            S([N("D"), N("E")]),
            [S([N("D"), N("E"), N("C")])],
        ),
        (
            S([N("A"), N("B"), N("A")]),
            S([N("A")]),
            S([N("X")]),
            [S([N("X"), N("B"), N("A")]), S([N("A"), N("B"), N("X")])],
        )
    ]
)
def test_apply(string, lhs, rhs, expected):
    rule = Rule(lhs, rhs)
    result = [i for i in rule.apply(string)]
    assert result == expected