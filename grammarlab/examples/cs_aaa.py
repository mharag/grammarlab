#!/usr/bin/python3
"""Context-Sensitive grammar for the language :math:`L = \\{a^n\\_a^n\\_a^n | n > 0\\}`.

"""

from grammarlab.core.app import App
from grammarlab.grammars.compact_definition import CS

N = {"S", "-", "A", "L", "R", "F"}
T = {"a", "_"}
P = [
    ("S", "a-L-a"),
    ("L-", "F_"),
    ("AL", "LA"),
    ("RA", "AR"),
    ("-L", "a-AR"),
    ("R-", "L-a"),
    ("AF", "Fa"),
    ("-F", "_a"),
]
S = "S"

grammar = CS(N, T, P, S)

if __name__ == "__main__":
    App(grammar).run()
