# Scattered Context Grammar that generates language L = {a^nb^n | n>= 0}

from glab.core.cli import App
from glab.export.code import CodeExport
from glab.grammars.grammars import SCG

N = {"S", "A", "B", "X"}
T = {"a", "b"}
P = [
    (["S"], ["AB"]),
    (["A", "B"], ["Aa", "Bb"]),
    (["A", "B"], ["a", "b"]),
]
S = "S"


grammar = SCG(N, T, P, S)

print(CodeExport().export(grammar))

if __name__ == "__main__":
    App(grammar).run()
