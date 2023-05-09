#!/usr/bin/python3
"""Example of verbose definition of grammar.

Grammar produces Dyck language. https://en.wikipedia.org/wiki/Dyck_language
Equivalent grammar defined in compact style can be found in :mod:`grammarlab.examples.cf_dyck`.

"""

from grammarlab.core.app import App
from grammarlab.core.common import Alphabet, NonTerminal, String, Terminal
from grammarlab.grammars.phrase_grammar import PhraseGrammar, PhraseRule

N = Alphabet({NonTerminal("S")})
T = Alphabet({Terminal("("), Terminal(")")})
P = [
    PhraseRule(
        String([NonTerminal("S")]), String([Terminal("("), NonTerminal("S"), Terminal(")")])
    ),
    PhraseRule(
        String([NonTerminal("S")]), String([NonTerminal("S"), NonTerminal("S")])
    ),
    PhraseRule(
        String([NonTerminal("S")]), String([Terminal("("), Terminal(")")])),
]
S = NonTerminal("S")

grammar = PhraseGrammar(N, T, P, S)

if __name__ == "__main__":
    App(grammar).run()
