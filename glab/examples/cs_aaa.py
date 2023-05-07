# Context-Sensitive grammar that generates language L = {a^n_a^n_a^n | n>= 1}

from glab.core.app import App
from glab.grammars.grammars import CS

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
