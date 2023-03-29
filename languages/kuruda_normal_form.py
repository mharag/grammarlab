from grammars.grammars import CS
from glab.cli import App

N = {"A", "B", "C", "D"}
T = {"a"}
P = [
    ("AB", "CD"),
    ("A", "BC"),
    ("A", "a"),
    ("A", "")
]
S = "A"

grammar = CS(N, T, P, S)

if __name__ == "__main__":
    App(grammar).run()