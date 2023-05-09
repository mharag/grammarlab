from glab.core.alphabet import Alphabet, NonTerminal, Terminal
from glab.core.config import STRING_DELIMITER
from glab.export.cli import CliExport
from glab.grammars.phrase_grammar import PhraseConfiguration, PhraseRule
from glab.grammars.scattered_context_grammar import ScatteredContextRule

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
