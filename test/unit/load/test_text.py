from glab.core.alphabet import Alphabet, NonTerminal, String, Terminal
from glab.grammars.pc_grammar_system import PCConfiguration, PCGrammarSystem
from glab.grammars.phrase_grammar import PhraseConfiguration, PhraseGrammar
from glab.load.text import TextLoad

a = Terminal("a")
A = NonTerminal("A")
alphabet = Alphabet({a, A})


def test_string():
    assert TextLoad().load(String, "aa", alphabet) == a + a


def test_phrase_configuration():
    grammar = PhraseGrammar(Alphabet({A}), Alphabet({a}), [], A)
    assert TextLoad().load(PhraseConfiguration, "aa", grammar) == PhraseConfiguration(a + a)
    assert TextLoad().load(PhraseConfiguration, "a#a", grammar, delimiter="#") == PhraseConfiguration(a + a)


def test_pc_configuration():
    c_1 = PhraseGrammar(Alphabet({A}), Alphabet({a}), [], A)
    c_2 = PhraseGrammar(Alphabet({A}), Alphabet({a}), [], A)
    grammar_system = PCGrammarSystem([NonTerminal("1"), NonTerminal("2")], [c_1, c_2])
    configuration = TextLoad().load(PCConfiguration, "a a  A A", grammar_system, delimiter=" ")
    assert configuration[0].sential_form == a + a
    assert configuration[1].sential_form == A + A
