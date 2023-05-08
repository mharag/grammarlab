#!/usr/bin/python3
"""PC grammar system for the language :math:`L = \\{a^{2^n} | n > 0\\}`.

Inspired by: https://cs.uwaterloo.ca/~lila/pdfs/Parallel%20communicating%20systems.pdf

"""

from glab.core.app import App
from glab.grammars.grammars import CF, PC

K = ["Q_1", "Q_2", "Q_3"]

# first component
P_1 = [
    (["S_1"], "aB"),
    (["S_1"], ["Q_2"]),
    (["B_1"], "B"),
    (["B_1"], [None]),
]
G_1 = CF({"S_1", "B", "B_1", "Q_2"}, {"a"}, P_1, "S_1")

# second component
P_2 = [
    (["S_2"], ["Q_1"]),
    (["B"], ["Q_3"]),
]
G_2 = CF({"S_2", "B", "Q_1", "Q_3"}, {"a"}, P_2, "S_2")

# third component
P_3 = [
    (["S_3"], ["Q_1"]),
    (["B"], ["B_1"]),
]
G_3 = CF({"S_3", "Q_1", "B", "B_1"}, {"a"}, P_3, "S_3")

grammar = PC(K, G_1, G_2, G_3)

if __name__ == "__main__":
    App(grammar).run()