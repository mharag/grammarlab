import pytest

from grammars.pc_grammar_system import PCGrammarSystemBase, Configuration
from grammars.scattered_context_grammar import ScatteredContextGrammar, ScatteredContextRule
from glab.alphabet import N, T, C, S


def test_g_step():
    grammar = ScatteredContextGrammar(
        [N("A")],
        [T("a")],
        [ScatteredContextRule([N("A")], [S([T("a")])])],
        N("A")
    )
    grammar1 = ScatteredContextGrammar(
        [N("B")],
        [T("b")],
        [ScatteredContextRule([N("B")], [S([T("b")])])],
        N("B")
    )

    pcgs = PCGrammarSystemBase(
        components=[grammar, grammar1]
    )
    configuration = Configuration([S([N("A"), N("A")]), S([N("B"), N("B")])])
    result = [x for x in pcgs.g_step(configuration)]

    expected = [
        Configuration([S([T("a"), N("A")]), S([T("b"), N("B")])]),
        Configuration([S([N("A"), T("a")]), S([T("b"), N("B")])]),
        Configuration([S([T("a"), N("A")]), S([N("B"), T("b")])]),
        Configuration([S([N("A"), T("a")]), S([N("B"), T("b")])]),
    ]
    assert result == expected

    configuration = Configuration([S([N("A"), N("A")]), S([N("C")])])
    with pytest.raises(Exception):
        next(pcgs.g_step(configuration))


def test_c_step():
    grammar1 = ScatteredContextGrammar(None, None, None, N("S1"))
    grammar2 = ScatteredContextGrammar(None, None, None, N("S2"))
    pcgs = PCGrammarSystemBase(components=[grammar1, grammar2])
    configuration = Configuration([S([C("1")]), S([N("B"), N("B")])])
    result = [x for x in pcgs.c_step(configuration)]
    assert len(result) == 1
    assert result[0] == Configuration([S([N("B"), N("B")]), S([N("S2")])])


    configuration = Configuration([S([C("1"), C("1")]), S([N("A"), N("B")])])
    result = [x for x in pcgs.c_step(configuration)]
    assert len(result) == 1
    assert result[0] == Configuration([S([N("A"), N("B"), N("A"), N("B")]), S([N("S2")])])

    configuration = Configuration([S([C("1"), C("1")]), S([C("0"), N("B")])])
    result = [x for x in pcgs.c_step(configuration)]
    assert len(result) == 0
