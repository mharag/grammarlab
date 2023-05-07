import pytest

from glab.core.alphabet import Alphabet as A
from glab.core.alphabet import NonTerminal
from glab.core.alphabet import String as S
from glab.core.alphabet import Terminal as T
from glab.grammars.phrase_grammar import PhraseConfiguration as C
from glab.grammars.phrase_grammar import PhraseGrammar as Grammar
from glab.grammars.phrase_grammar import PhraseGrammarRule as Rule


@pytest.mark.parametrize(
    "string,lhs,expected",
    [
        (
            S([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")]),
            S([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")]),
            [0]
        ),
        (
            S([NonTerminal("A"), NonTerminal("A"), NonTerminal("A")]),
            S([NonTerminal("A"), NonTerminal("A")]),
            [0, 1]
        ),
        (
            S([NonTerminal("A"), NonTerminal("A"), NonTerminal("A")]),
            S([NonTerminal("X")]),
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
            C(S([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")])),
            S([NonTerminal("A")]),
            S([NonTerminal("X"), NonTerminal("Y"), NonTerminal("Z")]),
            [C(S([NonTerminal("X"), NonTerminal("Y"), NonTerminal("Z"), NonTerminal("B"), NonTerminal("C")]))],
        ),
        (
            C(S([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")])),
            S([NonTerminal("A"), NonTerminal("B")]),
            S([NonTerminal("D"), NonTerminal("E")]),
            [C(S([NonTerminal("D"), NonTerminal("E"), NonTerminal("C")]))],
        ),
        (
            C(S([NonTerminal("A"), NonTerminal("B"), NonTerminal("A")])),
            S([NonTerminal("A")]),
            S([NonTerminal("X")]),
            [C(S([NonTerminal("X"), NonTerminal("B"), NonTerminal("A")])), C(S([NonTerminal("A"), NonTerminal("B"), NonTerminal("X")]))],
        )
    ]
)
def test_apply(string, lhs, rhs, expected):
    rule = Rule(lhs, rhs)
    result = list(rule.apply(string))
    assert result == expected


def test_derive():
    non_terminals = A({NonTerminal("S"), NonTerminal("A"), NonTerminal("X"), NonTerminal("B")})
    terminals = A({T("a"), T("b"), T("x")})
    rules = [
        Rule(S([NonTerminal("S")]), S([NonTerminal("A"), NonTerminal("A"), NonTerminal("X"), NonTerminal("A")])),
        Rule(S([NonTerminal("A")]), S([T("b"), T("b")])),
        Rule(S([NonTerminal("A"), NonTerminal("X"), NonTerminal("A")]), S([T("x")])),
    ]
    grammar = Grammar(non_terminals, terminals, rules, NonTerminal("S"))
    result = list(grammar.derive(100))
    assert result == [C(S([T("b"), T("b"), T("x")])), C(S([T("b"), T("b"), T("x")]))]
