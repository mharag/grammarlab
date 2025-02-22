#!/usr/bin/python3
"""Context-Sensitive grammar for the Dyck language.

"""

from grammarlab.core.app import App
from grammarlab.grammars.compact_definition import CF

N = {"S"}
T = {"(", ")"}
P = [
    ("S", "(S)"),
    ("S", "SS"),
    ("S", "()"),
]
S = "S"

grammar = CF(N, T, P, S)

if __name__ == "__main__":
    App(grammar).run()
