from glab.cli import App
from grammars.grammars import CF

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
