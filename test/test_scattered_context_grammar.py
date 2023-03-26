from generator.scattered_context_grammar import ScatteredContextRule, Rule
from generator.alphabet import N, S
import pytest


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
    matches = [match for match in rule.match(string)]

    assert matches == expected

@pytest.mark.parametrize(
    "string,rule,expected",
    [
        (
            S([N("A"), N("A"), N("A")]),
            Rule([N("A")], [S([N("B"), N("C")])]),
            [
                S([N("B"), N("C"), N("A"), N("A")]),
                S([N("A"), N("B"), N("C"), N("A")]),
                S([N("A"), N("A"), N("B"), N("C")]),
            ]
        ),
        (
            S([N("A"), N("B")]),
            Rule([N("A"), N("B")], [S([N("C")]), S([N("D")])]),
            [
                S([N("C"), N("D")]),
            ]
        )
    ]
)
def test_apply(string, rule, expected):
    derived = [match for match in rule.apply(string)]
    assert derived == expected
