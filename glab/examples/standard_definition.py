# Standard definition of the phrase grammar

from glab.core.alphabet import Alphabet, NonTerminal, String, Terminal
from glab.core.cli import App
from glab.grammars.phrase_grammar import PhraseGrammar, PhraseGrammarRule

N = Alphabet({NonTerminal("S")})
T = Alphabet({Terminal("("), Terminal(")")})
P = [
    PhraseGrammarRule(
        String([NonTerminal("S")]), String([Terminal("("), NonTerminal("S"), Terminal(")")])
    ),
    PhraseGrammarRule(
        String([NonTerminal("S")]), String([NonTerminal("S"), NonTerminal("S")])
    ),
    PhraseGrammarRule(
        String([NonTerminal("S")]), String([Terminal("("), Terminal(")")])),
]
S = NonTerminal("S")

grammar = PhraseGrammar(N, T, P, S)

if __name__ == "__main__":
    App(grammar).run()
