from glab.core.app import App
from glab.grammars.grammars import CF, PC

K = ["Q_1", "Q_2", "Q_3"]

N_1 = {"S_1", "B", "B_1", "Q_2"}
T_1 = {"a"}
P_1 = [
    (["S_1"], "aB"),
    (["S_1"], ["Q_2"]),
    (["B_1"], "B"),
    (["B_1"], [None]),
]
S_1 = "S_1"

G_1 = CF(N_1, T_1, P_1, S_1)

N_2 = {"S_2", "B", "Q_1", "Q_3"}
T_2 = {"a"}
P_2 = [
    (["S_2"], ["Q_1"]),
    (["B"], ["Q_3"]),
]
S_2 = "S_2"

G_2 = CF(N_2, T_2, P_2, S_2)

N_3 = {"S_3", "Q_1", "B", "B_1"}
T_3 = {"a"}
P_3 = [
    (["S_3"], ["Q_1"]),
    (["B"], ["B_1"]),
]
S_3 = "S_3"

G_3 = CF(N_3, T_3, P_3, S_3)

G = PC(K, G_1, G_2, G_3)

if __name__ == "__main__":
    App(G).run()