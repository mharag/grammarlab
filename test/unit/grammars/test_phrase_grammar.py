import pytest

from glab.alphabet import A, N, S, T
from grammars.phrase_grammar import PhraseConfiguration as C
from grammars.phrase_grammar import PhraseGrammar as Grammar
from grammars.phrase_grammar import PhraseGrammarRule as Rule


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
    result = list(rule.match(string))
    assert result == expected


@pytest.mark.parametrize(
    "string,lhs,rhs,expected",
    [
        (
            C(S([N("A"), N("B"), N("C")])),
            S([N("A")]),
            S([N("X"), N("Y"), N("Z")]),
            [C(S([N("X"), N("Y"), N("Z"), N("B"), N("C")]))],
        ),
        (
            C(S([N("A"), N("B"), N("C")])),
            S([N("A"), N("B")]),
            S([N("D"), N("E")]),
            [C(S([N("D"), N("E"), N("C")]))],
        ),
        (
            C(S([N("A"), N("B"), N("A")])),
            S([N("A")]),
            S([N("X")]),
            [C(S([N("X"), N("B"), N("A")])), C(S([N("A"), N("B"), N("X")]))],
        )
    ]
)
def test_apply(string, lhs, rhs, expected):
    rule = Rule(lhs, rhs)
    result = list(rule.apply(string))
    assert result == expected


def test_derive():
    non_terminals = A({N("S"), N("A"), N("X"), N("B")})
    terminals = A({T("a"), T("b"), T("x")})
    rules = [
        Rule(S([N("S")]), S([N("A"),  N("A"), N("X"), N("A")])),
        Rule(S([N("A")]), S([T("b"), T("b")])),
        Rule(S([N("A"), N("X"), N("A")]), S([T("x")])),
    ]
    grammar = Grammar(non_terminals, terminals, rules, N("S"))
    result = list(grammar.derive(100))
    assert result == [C(S([T("b"), T("b"), T("x")])), C(S([T("b"), T("b"), T("x")]))]
