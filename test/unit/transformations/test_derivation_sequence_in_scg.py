from grammarlab.grammars.scattered_context_grammar import SCGConfiguration as Conf
from grammarlab.transformations.derivation_sequence_in_scg import (
    N,
    T,
    finish_left_to_right,
    non_terminal_before_working_space,
    symbol_not_copied,
)


def test_non_terminal_before_working_space():
    left = N("[")
    terminal = T("a").terminal
    non_terminal = T("A").non_terminal

    assert non_terminal_before_working_space(Conf(terminal + left))
    assert not non_terminal_before_working_space(Conf(non_terminal + left))
    assert not non_terminal_before_working_space(Conf(terminal + non_terminal + terminal + left))
    assert non_terminal_before_working_space(Conf(left + non_terminal))


def test_symbol_not_copied():
    state = N("Q_3")
    terminal = T("a").terminal
    non_terminal = T("A").non_terminal
    pointer = T("A").pointer

    assert symbol_not_copied(Conf(state + terminal))
    assert symbol_not_copied(Conf(state + terminal + pointer))
    assert not symbol_not_copied(Conf(state + non_terminal + pointer))


def test_finish_left_to_right():
    state = N("Q_7")
    terminal = T("a").terminal
    non_terminal = T("A").non_terminal
    left = N("[")

    assert finish_left_to_right(Conf(state + terminal + left + terminal))
    assert finish_left_to_right(Conf(state + terminal + left + non_terminal))
    assert finish_left_to_right(Conf(state + terminal + left + terminal + non_terminal))
    assert not finish_left_to_right(Conf(state + terminal + left + non_terminal + terminal))
