#!/usr/bin/python3
"""Non-returning PC grammar system for the language :math:`L = \\{\\_a^1\\_a^2\\_ \dots \\_a^n\\_ | n \geq 0\\}`.

"""

from glab.core.app import App
from glab.grammars.compact_definition import CF, NPC

K = ["1", "2"]
N_1 = {"A", "2"}
T_1 = {"a", "-"}
P_1 = [
    ("A", "-2"),
    ("A", "-"),
]
S_1 = "A"

C_1 = CF(N_1, T_1, P_1, S_1)

N_2 = {"A"}
T_2 = {"a"}
P_2 = [
    ("A", "aA")
]
S_2 = "A"

C_2 = CF(N_2, T_2, P_2, S_2)

G = NPC(K, C_1, C_2)

if __name__ == "__main__":
    App(G).run()
