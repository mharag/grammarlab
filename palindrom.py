from glab.core.alphabet import Alphabet, NonTerminal
from glab.core.alphabet import String as Str
from glab.core.alphabet import Terminal
from glab.core.cli import App
from glab.grammars.phrase_grammar import PhraseGrammar
from glab.grammars.phrase_grammar import PhraseGrammarRule as Rule

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
