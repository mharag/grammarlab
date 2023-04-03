import pytest

from glab.alphabet import N, S, T
from grammars.pc_grammar_system import PCConfiguration, PCGrammarSystem
from grammars.scattered_context_grammar import (ScatteredContextGrammar,
                                                ScatteredContextRule)
from grammars.scattered_context_grammar import SCGConfiguration as C


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
    configuration = PCConfiguration([C(S([N("A"), N("A")])), C(S([N("B"), N("B")]))])
    result = list(pcgs.g_step(configuration))

    expected = [
        PCConfiguration([C(S([T("a"), N("A")])), C(S([T("b"), N("B")]))]),
        PCConfiguration([C(S([N("A"), T("a")])), C(S([T("b"), N("B")]))]),
        PCConfiguration([C(S([T("a"), N("A")])), C(S([N("B"), T("b")]))]),
        PCConfiguration([C(S([N("A"), T("a")])), C(S([N("B"), T("b")]))]),
    ]
    print(result)
    assert result == expected

    configuration = PCConfiguration([C(S([N("A"), N("A")])), C(S([N("C")]))])
    with pytest.raises(Exception):
        next(pcgs.g_step(configuration))


def test_c_step():
    grammar1 = ScatteredContextGrammar(None, None, None, N("S1"))
    grammar2 = ScatteredContextGrammar(None, None, None, N("S2"))
    pcgs = PCGrammarSystem(
        comumunication_symbols=[N("1"), N("2")],
        components=[grammar1, grammar2]
    )
    configuration = PCConfiguration([C(S([N("2")])), C(S([N("B"), N("B")]))])
    result = list(pcgs.c_step(configuration))
    assert len(result) == 1
    assert result[0] == PCConfiguration([C(S([N("B"), N("B")])), C(S([N("S2")]))])

    configuration = PCConfiguration([C(S([N("2"), N("2")])), C(S([N("A"), N("B")]))])
    result = list(pcgs.c_step(configuration))
    assert len(result) == 1
    assert result[0] == PCConfiguration([C(S([N("A"), N("B"), N("A"), N("B")])), C(S([N("S2")]))])

    configuration = PCConfiguration([C(S([N("2"), N("2")])), C(S([N("1"), N("1")]))])
    result = list(pcgs.c_step(configuration))
    assert len(result) == 0
