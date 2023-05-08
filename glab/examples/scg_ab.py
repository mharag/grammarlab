#!/usr/bin/python3
"""Scattered Context Grammar for the language :math:`L = \\{a^nb^n | n > 0\\}`.

"""

from glab.core.app import App
from glab.grammars.compact_definition import SCG

N = {"S", "A", "B", "X"}
T = {"a", "b"}
P = [
    (["S"], ["AB"]),
    (["A", "B"], ["Aa", "Bb"]),
    (["A", "B"], ["a", "b"]),
]
S = "S"


grammar = SCG(N, T, P, S)

if __name__ == "__main__":
    App(grammar).run()
