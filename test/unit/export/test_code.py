from glab.core.alphabet import Alphabet, NonTerminal, Terminal
from glab.export.code import CodeExport
from glab.grammars.phrase_grammar import PhraseRule
from glab.grammars.scattered_context_grammar import ScatteredContextRule

a = Terminal("a")
A = NonTerminal("A")


def test_string():
    assert CodeExport().export(a+a) == '"aa"'
    assert CodeExport().export(a+Terminal("A_1")) == '["a", "A_1"]'


def test_alphabet():
    assert CodeExport().export(Alphabet({a})) == '{"a"}'


def test_phrase_rule():
    assert CodeExport().export(PhraseRule(A+A, a+a)) == '("AA", "aa")'
    assert CodeExport().export(PhraseRule(A+A, a+Terminal("a_1"))) == '("AA", ["a", "a_1"])'


def test_scattered_context_rule():
    assert CodeExport().export(ScatteredContextRule([A, A], [a+a, a+a])) == '(["A", "A"], ["aa", "aa"])'
