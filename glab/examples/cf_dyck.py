# Context-free grammar that generates the language of Dyck words

from glab.core.app import App
from glab.grammars.grammars import CF

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
