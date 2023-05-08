#!/usr/bin/python3
"""Example of Context-Sensitive grammar in Kuruda normal form.

Grammar produces language :math:`L = \\{a^n | n > 0\\}`.

"""

from glab.core.app import App
from glab.grammars.compact_definition import CF

N = {"A", "B"}
T = {"a"}
P = [
    ("A", "a"),
    ("A", "Aa"),
]
S = "A"

grammar = CF(N, T, P, S)

if __name__ == "__main__":
    App(grammar).run()
