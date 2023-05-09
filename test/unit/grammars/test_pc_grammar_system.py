import pytest

from grammarlab.core.common import NonTerminal
from grammarlab.core.common import String as S
from grammarlab.core.common import Terminal as T
from grammarlab.grammars.pc_grammar_system import PCConfiguration, PCGrammarSystem
from grammarlab.grammars.scattered_context_grammar import (
    ScatteredContextGrammar,
    ScatteredContextRule,
)
from grammarlab.grammars.scattered_context_grammar import SCGConfiguration as C


def test_g_step():
    grammar = ScatteredContextGrammar(
        [NonTerminal("A")],
        [T("a")],
        [ScatteredContextRule([NonTerminal("A")], [S([T("a")])])],
        NonTerminal("A")
    )
    grammar1 = ScatteredContextGrammar(
        [NonTerminal("B")],
        [T("b")],
        [ScatteredContextRule([NonTerminal("B")], [S([T("b")])])],
        NonTerminal("B")
    )

    pcgs = PCGrammarSystem(
        comumunication_symbols=[NonTerminal("1"), NonTerminal("2")],
        components=[grammar, grammar1]
    )
    configuration = PCConfiguration([C(S([NonTerminal("A"), NonTerminal("A")])), C(S([NonTerminal("B"), NonTerminal("B")]))])
    result = list(pcgs.g_step(configuration))

    expected = [
        PCConfiguration([C(S([T("a"), NonTerminal("A")])), C(S([T("b"), NonTerminal("B")]))]),
        PCConfiguration([C(S([NonTerminal("A"), T("a")])), C(S([T("b"), NonTerminal("B")]))]),
        PCConfiguration([C(S([T("a"), NonTerminal("A")])), C(S([NonTerminal("B"), T("b")]))]),
        PCConfiguration([C(S([NonTerminal("A"), T("a")])), C(S([NonTerminal("B"), T("b")]))]),
    ]
    print(result)
    print(expected)
    assert result == expected

    configuration = PCConfiguration([C(S([NonTerminal("A"), NonTerminal("A")])), C(S([NonTerminal("C")]))])
    with pytest.raises(Exception):
        next(pcgs.g_step(configuration))


def test_c_step():
    grammar1 = ScatteredContextGrammar(None, None, None, NonTerminal("S1"))
    grammar2 = ScatteredContextGrammar(None, None, None, NonTerminal("S2"))
    pcgs = PCGrammarSystem(
        comumunication_symbols=[NonTerminal("1"), NonTerminal("2")],
        components=[grammar1, grammar2]
    )
    configuration = PCConfiguration([C(S([NonTerminal("2")])), C(S([NonTerminal("B"), NonTerminal("B")]))])
    result = list(pcgs.c_step(configuration))
    assert len(result) == 1
    assert result[0] == PCConfiguration([C(S([NonTerminal("B"), NonTerminal("B")])), C(S([NonTerminal("S2")]))])

    configuration = PCConfiguration([C(S([NonTerminal("2"), NonTerminal("2")])), C(S([NonTerminal("A"), NonTerminal("B")]))])
    result = list(pcgs.c_step(configuration))
    assert len(result) == 1
    assert result[0] == PCConfiguration([C(S([NonTerminal("A"), NonTerminal("B"), NonTerminal("A"), NonTerminal("B")])), C(S([NonTerminal("S2")]))])

    configuration = PCConfiguration([C(S([NonTerminal("2"), NonTerminal("2")])), C(S([NonTerminal("1"), NonTerminal("1")]))])
    result = list(pcgs.c_step(configuration))
    assert len(result) == 0
