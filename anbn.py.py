from grammar.grammars import SCG

N = {"S", "A", "B", "X"}
T = {"a", "b"}
P = [
    (["S"], ["AB"]),
    (["A", "B"], ["Aa", "Bb"]),
    (["A", "B"], ["a", "b"]),
]
S = "S"

an_bn = SCG(N, T, P, S).run()
