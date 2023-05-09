from grammarlab.core.common import Alphabet, NonTerminal, Terminal
from grammarlab.core.config import STRING_DELIMITER
from grammarlab.export.cli import CliExport
from grammarlab.grammars.phrase_grammar import PhraseConfiguration, PhraseRule
from grammarlab.grammars.scattered_context_grammar import ScatteredContextRule

a = Terminal("a")
A = NonTerminal("A")


def test_symbol():
    assert CliExport().export(a) == "a"


def test_alphabet():
    assert CliExport().export(Alphabet({a})) == "{a}"


def test_string():
    assert CliExport().export(a+a+A+A) == STRING_DELIMITER.join("aaAA")


def test_phrase_rule():
    assert CliExport().export(PhraseRule(A+A, a+a)) == "A A -> a a"


def test_scattered_context_rule():
    assert CliExport().export(ScatteredContextRule([A, A], [a, a])) == "(A,A) -> (a,a)"


def test_phrase_configuration():
    assert CliExport().export(PhraseConfiguration(A+A)) == STRING_DELIMITER.join("AA")
