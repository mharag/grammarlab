from grammarlab.core.app import App
from grammarlab.core.common import Alphabet, NonTerminal
from grammarlab.core.common import String as Str
from grammarlab.core.common import Terminal
from grammarlab.grammars.phrase_grammar import PhraseGrammar
from grammarlab.grammars.phrase_grammar import PhraseRule as Rule

alphabet = {"a", "b", "c", "d", "e"}
terminals = Alphabet({Terminal(x) for x in alphabet})
S = NonTerminal("S")
rules = [
    *[Rule(Str([S]), X+S+X) for X in terminals],
    *[Rule(Str([S]), X+X) for X in terminals]
]
grammar = PhraseGrammar(Alphabet({S}), terminals, rules, S)

if __name__ == "__main__":
    App(grammar).run()
