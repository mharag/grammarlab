from grammars.pc_grammar_system import PCGrammarSystem
from glab.alphabet import N,T,Alphabet, String
from grammars.scattered_context_grammar import ScatteredContextGrammar as Grammar, ScatteredContextRule as Rule
import itertools


def color(text):
    return f"\033[32m{text}\033[0m"


class Symbol:
    def __init__(self, original_symbol):
        self.original_symbol = original_symbol

    @property
    def comm(self):
        return N(f"{self.original_symbol}{color('_C')}")

    @property
    def end(self):
        return N(f"{self.original_symbol}{color('_E')}'")

    @property
    def current(self):
        return N(f"{self.original_symbol}{color('^*')}")

    @property
    def terminal(self):
        if type(self.original_symbol) == T:
            return self.original_symbol
        raise ValueError("Traing to convert non terminal to terminal!")

    @property
    def non_terminal(self):
        return N(f"{self.original_symbol}{color('_O')}") if type(self.original_symbol) == N else N(f"{self.original_symbol}{color('_T')}")


def construct_grammar(G, separator):
    N_G = G.non_terminals
    T_G = G.terminals
    P_G = G.rules
    S_G = G.start_symbol
    n_alphabet = {Symbol(x) for x in N_G}
    t_alphabet = {Symbol(x) for x in T_G}
    alphabet = n_alphabet | t_alphabet
    S_O = Symbol(S_G)
    separator = Symbol(separator)

    W = N("W")
    E = T("-")
    N_comm = {x.comm for x in alphabet}
    N_end = {x.end for x in alphabet}
    N_current = {x.current for x in alphabet}
    N_O = {x.non_terminal for x in n_alphabet}
    N_T = {x.non_terminal for x in t_alphabet}
    T_H = {x.terminal for x in t_alphabet}

    Q_A = N("Q_A")
    Q_B = N("Q_B")
    Q_C = N("Q_C")
    K = [Q_A, Q_B, Q_C]

    S_C = N("S_C")
    P_C = [
        Rule([S_C], [W])
    ]
    for symbol in t_alphabet:
        P_C.extend([
            Rule([S_C], [symbol.comm]),
            Rule([symbol.comm], [symbol.comm]),
            Rule([S_C], [symbol.end]),
            Rule([symbol.end], [symbol.end]),
        ])

    C = Grammar(N_comm | N_end | {S_C, W}, set(), P_C, S_C)

    S_A = N("S_A")
    P_A = [
        Rule([S_A], [Q_C]),
        Rule([W], [W]),
    ]
    for symbol in t_alphabet:
        P_A.extend([
            Rule([symbol.comm], [symbol.terminal + Q_C]),
            Rule([symbol.end], [symbol.non_terminal]),
            Rule([symbol.non_terminal], [symbol.terminal]),
        ])

    A = Grammar(N_comm | N_end | {S_A, W} | N_T, T_H, P_A, S_A)

    S_B = N("S_B")
    R_0, R_1, R_2, R_3 = N("R_0"), N("R_1"), N("R_2"), N("R_3")
    R = {R_0, R_1, R_2, R_3}
    P_B = [
        Rule([S_B], [R_0 + Q_C]),
        Rule([R_0, W], [R_1, S_O.non_terminal]),
        Rule([R_1], [R_2]),
        Rule([R_2], [R_3 + Q_A])
    ]
    ignore = [T("*")]
    for rule in P_G:
        P_B.append(
            Rule(
                [R_1] + [Symbol(x).non_terminal for x in rule.lhs],
                [R_1] + [
                    String(
                        [
                            Symbol(x).non_terminal if x not in ignore else Symbol(x).terminal
                            for x in string
                        ]
                    )
                    for string in rule.rhs
                ],
            )
        )

    for symbol in t_alphabet:
        P_B.extend([
            Rule(
                [R_2, symbol.non_terminal, separator.non_terminal],
                [R_2, symbol.terminal, separator.non_terminal]
            ),
            Rule(
                [R_3, W, separator.non_terminal, symbol.non_terminal],
                [R_3, Q_C, separator.terminal, symbol.current],
            ),
            Rule(
                [R_3, symbol.end, symbol.current],
                [E, E, E]
            )
        ])

    for X, Y in itertools.product(t_alphabet, t_alphabet):
        P_B.append(
            Rule(
                [R_3, X.comm, X.current, Y.non_terminal],
                [R_3, Q_C, X.terminal, Y.current]
            )
        )

    B = Grammar(
        N_comm | N_end | {S_B, W} | N_T | N_current | {Q_A, Q_C} | R,
        T_H,
        P_B,
        S_B
    )

    return PCGrammarSystem(K, [A, B, C])

