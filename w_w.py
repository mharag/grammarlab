from grammar.grammars import CS

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

grammar = CS(N, T, P, S).run()
