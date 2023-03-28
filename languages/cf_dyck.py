from grammars.grammars import CF
from glab.cli import App

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
