import pytest

from glab.alphabet import NonTerminal, S, T
from grammars.scattered_context_grammar import Rule
from grammars.scattered_context_grammar import \
    ScatteredContextGrammar as Grammar
from grammars.scattered_context_grammar import ScatteredContextRule
from grammars.scattered_context_grammar import SCGConfiguration as C


def test_find_next():
    index = {
        "A": [1, 10, 20]
    }
    assert ScatteredContextRule.find_next(index=index, string_position=0, last=-1, symbol="A") == 0
    assert ScatteredContextRule.find_next(index=index, string_position=1, last=-1, symbol="A") == 1
    assert ScatteredContextRule.find_next(index=index, string_position=1, last=1, symbol="A") == 2
    assert ScatteredContextRule.find_next(index=index, string_position=1, last=2, symbol="A") == -1

@pytest.mark.parametrize(
    "string,rule,expected",
    [
        (
            S([NonTerminal("A"), NonTerminal("A"), NonTerminal("A")]),
            [NonTerminal("B")],
            []
        ),
        (
            S([NonTerminal("A"), NonTerminal("A"), NonTerminal("A")]),
            [NonTerminal("A")],
            [[0], [1], [2]]
        ),
        (
            S([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")]),
            [NonTerminal("A"), NonTerminal("B"), NonTerminal("C")],
            [[0, 1, 2]]
        ),
        (
            S([NonTerminal("A"), NonTerminal("A"), NonTerminal("B"), NonTerminal("C"), NonTerminal("C")]),
            [NonTerminal("A"), NonTerminal("B"), NonTerminal("C")],
            [[0, 2, 3], [0, 2, 4], [1, 2, 3], [1, 2, 4]]
        )
    ]
)
def test_match_single(string, rule, expected):
    rule = ScatteredContextRule(rule, [S([])]*len(rule))
    matches = list(rule.match(string))

    assert matches == expected

@pytest.mark.parametrize(
    "string,rule,expected",
    [
        (
            C(S([NonTerminal("A"), NonTerminal("A"), NonTerminal("A")])),
            Rule([NonTerminal("A")], [S([NonTerminal("B"), NonTerminal("C")])]),
            [
                C(S([NonTerminal("B"), NonTerminal("C"), NonTerminal("A"), NonTerminal("A")])),
                C(S([NonTerminal("A"), NonTerminal("B"), NonTerminal("C"), NonTerminal("A")])),
                C(S([NonTerminal("A"), NonTerminal("A"), NonTerminal("B"), NonTerminal("C")])),
            ]
        ),
        (
            C(S([NonTerminal("A"), NonTerminal("B")])),
            Rule([NonTerminal("A"), NonTerminal("B")], [S([NonTerminal("C")]), S([NonTerminal("D")])]),
            [
                C(S([NonTerminal("C"), NonTerminal("D")])),
            ]
        )
    ]
)
def test_apply(string, rule, expected):
    derived = list(rule.apply(string))
    assert derived == expected


def test_derive():
    rule1 = Rule([NonTerminal("A")], [S([T("a")])])
    rule2 = Rule([NonTerminal("A")], [S([NonTerminal("A"), T("a")])])

    grammar = Grammar(
        [NonTerminal("A")],
        [T("a")],
        [rule1, rule2],
        NonTerminal("A")
    )
    language = list(grammar.derive(10))
    control_language = [C(S([T("a")]*i)) for i in range(1, 11)]
    print(language)
    print(control_language)
    assert language == control_language
