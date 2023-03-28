from grammars.grammars import SCG
from glab.cli import App

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
