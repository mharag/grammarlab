import pytest

from glab.alphabet import N, S, T
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
            S([N("A"), N("A"), N("A")]),
            [N("B")],
            []
        ),
        (
            S([N("A"), N("A"), N("A")]),
            [N("A")],
            [[0], [1], [2]]
        ),
        (
            S([N("A"), N("B"), N("C")]),
            [N("A"), N("B"), N("C")],
            [[0, 1, 2]]
        ),
        (
            S([N("A"), N("A"), N("B"), N("C"), N("C")]),
            [N("A"), N("B"), N("C")],
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
            C(S([N("A"), N("A"), N("A")])),
            Rule([N("A")], [S([N("B"), N("C")])]),
            [
                C(S([N("B"), N("C"), N("A"), N("A")])),
                C(S([N("A"), N("B"), N("C"), N("A")])),
                C(S([N("A"), N("A"), N("B"), N("C")])),
            ]
        ),
        (
            C(S([N("A"), N("B")])),
            Rule([N("A"), N("B")], [S([N("C")]), S([N("D")])]),
            [
                C(S([N("C"), N("D")])),
            ]
        )
    ]
)
def test_apply(string, rule, expected):
    derived = list(rule.apply(string))
    assert derived == expected


def test_derive():
    rule1 = Rule([N("A")], [S([T("a")])])
    rule2 = Rule([N("A")], [S([N("A"), T("a")])])

    grammar = Grammar(
        [N("A")],
        [T("a")],
        [rule1, rule2],
        N("A")
    )
    language = list(grammar.derive(10))
    control_language = [C(S([T("a")]*i)) for i in range(1, 11)]
    print(language)
    print(control_language)
    assert language == control_language
