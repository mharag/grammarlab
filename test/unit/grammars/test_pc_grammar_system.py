import pytest

from grammars.pc_grammar_system import PCGrammarSystem, PCConfiguration
from grammars.scattered_context_grammar import ScatteredContextGrammar, ScatteredContextRule
from glab.alphabet import N, T, S


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

    pcgs = PCGrammarSystem(
        comumunication_symbols=[N("1"), N("2")],
        components=[grammar, grammar1]
    )
    configuration = PCConfiguration([S([N("A"), N("A")]), S([N("B"), N("B")])])
    result = [x for x in pcgs.g_step(configuration)]

    expected = [
        PCConfiguration([S([T("a"), N("A")]), S([T("b"), N("B")])]),
        PCConfiguration([S([N("A"), T("a")]), S([T("b"), N("B")])]),
        PCConfiguration([S([T("a"), N("A")]), S([N("B"), T("b")])]),
        PCConfiguration([S([N("A"), T("a")]), S([N("B"), T("b")])]),
    ]
    assert result == expected

    configuration = PCConfiguration([S([N("A"), N("A")]), S([N("C")])])
    with pytest.raises(Exception):
        next(pcgs.g_step(configuration))


def test_c_step():
    grammar1 = ScatteredContextGrammar(None, None, None, N("S1"))
    grammar2 = ScatteredContextGrammar(None, None, None, N("S2"))
    pcgs = PCGrammarSystem(
        comumunication_symbols=[N("1"), N("2")],
        components=[grammar1, grammar2]
    )
    configuration = PCConfiguration([S([N("2")]), S([N("B"), N("B")])])
    result = [x for x in pcgs.c_step(configuration)]
    assert len(result) == 1
    assert result[0] == PCConfiguration([S([N("B"), N("B")]), S([N("S2")])])

    configuration = PCConfiguration([S([N("2"), N("2")]), S([N("A"), N("B")])])
    result = [x for x in pcgs.c_step(configuration)]
    assert len(result) == 1
    assert result[0] == PCConfiguration([S([N("A"), N("B"), N("A"), N("B")]), S([N("S2")])])

    configuration = PCConfiguration([S([N("2"), N("2")]), S([N("1"), N("1")])])
    result = [x for x in pcgs.c_step(configuration)]
    assert len(result) == 0
