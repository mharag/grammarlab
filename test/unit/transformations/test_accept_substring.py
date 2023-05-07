from glab.grammars.pc_grammar_system import PCConfiguration as PCConf
from glab.grammars.phrase_grammar import PhraseConfiguration as PhraseConf
from glab.transformations.accept_substring import (
    N, T, communication_left_to_right, copy_after_finish,
    finish_from_left_to_right, finish_part_before_separator)


def test_copy_after_finish():
    state = N("R_2")
    terminal = T("a")
    non_terminal = N("A")

    assert copy_after_finish(
        PCConf([None, PhraseConf(state + terminal.terminal + terminal.non_terminal + terminal)])
    )
    assert not copy_after_finish(
        PCConf([None, PhraseConf(state + terminal.terminal + non_terminal.non_terminal + terminal)])
    )
    assert not copy_after_finish(
        PCConf([None, PhraseConf(state + terminal.terminal + non_terminal.terminal + terminal)])
    )


def test_finish_from_left_to_right():
    state = N("R_2")
    terminal = T("a")
    ignore = T("*")

    assert finish_from_left_to_right(
        PCConf([None, PhraseConf(state + terminal.terminal + terminal.non_terminal)])
    )
    assert not finish_from_left_to_right(
        PCConf([None, PhraseConf(state + terminal.non_terminal + terminal.terminal)])
    )
    assert finish_from_left_to_right(
        PCConf([None, PhraseConf(state + terminal.non_terminal + ignore.terminal + terminal.non_terminal)])
    )


def test_finish_part_before_separator():
    state = N("R_3")
    query = N("Q_A")
    terminal = T("a")
    delimiter = T("#")

    assert finish_part_before_separator(
        PCConf([None, PhraseConf(state + query + terminal.terminal + delimiter.non_terminal)])
    )
    assert not finish_part_before_separator(
        PCConf([None, PhraseConf(state + query + terminal.non_terminal + delimiter.non_terminal)])
    )
    assert not finish_part_before_separator(
        PCConf([None, PhraseConf(state + query + terminal.non_terminal + terminal.terminal + delimiter.non_terminal)])
    )


def test_communication_left_to_right():
    state = N("R_3")
    terminal = T("a")
    delimiter = T("#")
    ignore = T("*")

    assert communication_left_to_right(
        PCConf([None, PhraseConf(state + delimiter.terminal + terminal.terminal)])
    )
    assert not communication_left_to_right(
        PCConf([None, PhraseConf(state + delimiter.terminal + terminal.non_terminal + terminal.terminal)])
    )
    assert communication_left_to_right(
        PCConf([None, PhraseConf(state + delimiter.terminal + terminal.terminal + ignore.terminal)])
    )
