from grammars.scattered_context_grammar import ScatteredContextRule as Rule, ScatteredContextGrammar as Grammar
from glab.alphabet import S,Alphabet, SymbolType
from glab.extended_symbol import ExtendedSymbol, NonTerminal as N, Terminal as T
import itertools
from glab.config import GREEN


class SCGSymbol(ExtendedSymbol):
    color = GREEN
    variants = {
        "non_terminal": (SymbolType.NON_TERMINAL, "N"),
        "cs_left": (SymbolType.NON_TERMINAL, "<"),
        "cs_right": (SymbolType.NON_TERMINAL, ">"),
        "pointer": (SymbolType.NON_TERMINAL, "*"),
        "cs_left_pointer": (SymbolType.NON_TERMINAL, "<*"),
        "copied": (SymbolType.NON_TERMINAL, "+"),
    }

    @property
    def terminal(self):
        if self.type == SymbolType.TERMINAL:
            return SCGSymbol(self.base_symbol, "terminal", *self.base)
        return SCGSymbol(self.base_symbol, "terminal", SymbolType.TERMINAL, "T")


def construct_grammar(G):
    N_G = G.non_terminals
    T_G = G.terminals
    P_G = G.rules
    S_G = G.start_symbol

    N_extended = {SCGSymbol(x) for x in N_G}
    T_extended = {SCGSymbol(x) for x in T_G}
    alphabet_extended = N_extended | T_extended
    S_O = SCGSymbol(S_G).non_terminal

    S_H = N("S_H")
    Q_1, Q_2, Q_3, Q_4, Q_5, Q_6, Q_7 = N("Q_1"), N("Q_2"), N("Q_3"), N("Q_4"), N("Q_5"), N("Q_6"), N("Q_7")
    Q = {Q_1, Q_2, Q_3, Q_4, Q_5, Q_6}
    PL, PR, NL, NR = N("["), N("]"), N("<"), N(">")
    K = {PL, PR, NL, NR}
    N_H = Alphabet(
        {x.non_terminal for x in alphabet_extended}
        | {x.terminal for x in alphabet_extended}
        | {x.pointer for x in alphabet_extended}
        | {x.cs_left for x in N_extended}
        | {x.cs_left_pointer for x in N_extended}
        | {x.cs_right for x in N_extended}
        | {x.copied for x in N_extended}
        | Q | K | {S_H}
    )

    T_e = T("e")
    T_delim = T("*")
    T_sep = T("#")
    T_H = Alphabet(
        {x.terminal for x in alphabet_extended}
        | {T_e, T_delim, T_sep}
    )

    p_init = Rule([S_H], [Q_1 + PL + S_O + PR + NL + NR])

    P_Q1 = [Rule([Q_1], [Q_7])]
    for rule in P_G:
        lhs = [SCGSymbol(x) for x in rule.lhs]
        rhs = [SCGSymbol(x) for x in rule.rhs]
        if len(lhs) == 2 and len(rhs) == 2:
            A, B = lhs
            C, D = rhs
            lhs = [Q_1, PL, A.non_terminal, B.non_terminal, PR]
            rhs = [Q_2, PL, C.cs_left, D.cs_right, PR]
            P_Q1.append(Rule(lhs, rhs))
        elif len(lhs) == 1 and len(rhs) == 2:
            A = lhs[0]
            B, C = rhs
            lhs = [Q_1, PL, A.non_terminal, PR]
            rhs = [Q_4, PL, B.non_terminal + C.non_terminal, PR]
            P_Q1.append(Rule(lhs, rhs))
        elif len(lhs) == 1 and len(rhs) == 1:
            A = lhs[0]
            B = rhs[0]
            print(B)
            lhs = [Q_1, PL, A.non_terminal, PR]
            rhs = [Q_4, PL, B.non_terminal, PR]
            print(rhs)
            P_Q1.append(Rule(lhs, rhs))
        elif len(rule.lhs) == 1 and len(rule.rhs) == 0:
            A = rule.lhs[0]
            lhs = [Q_1, PL, A.non_terminal, PR]
            rhs = [Q_4, PL, T_e, PR]
            P_Q1.append(Rule(lhs, rhs))

    P_Q2 = []
    for symbol in N_extended:
        P_Q2.extend([
            Rule([Q_2, PL, symbol.non_terminal, PR], [Q_3, PL, symbol.pointer, PR]),
            Rule([Q_2, PL, symbol.cs_left, PR], [Q_3, PL, symbol.pointer, PR]),
        ])
    for symbol in T_extended:
        P_Q2.append(
            Rule([Q_2, PL, symbol.non_terminal, PR], [Q_3, PL, symbol.pointer, PR]),
        )

    P_Q3 = []
    for X, Y, C in itertools.product(alphabet_extended, alphabet_extended, N_extended):
        lhs = [Q_3, PL, X.pointer, Y.non_terminal, C.cs_left, PR, NR]
        rhs = [Q_3, PL, X.terminal, Y.pointer, C.cs_left, PR, X.non_terminal + NR]
        P_Q3.append(Rule(lhs, rhs))
    for X, C in itertools.product(alphabet_extended, N_extended):
        lhs = [Q_3, PL, X.pointer, C.cs_left, PR, NR]
        rhs = [Q_3, PL, X.terminal, C.cs_left_pointer, PR, X.non_terminal + NR]
        P_Q3.append(Rule(lhs, rhs))
    for C, D, X in itertools.product(N_extended, N_extended, alphabet_extended):
        lhs = [Q_3, PL, C.cs_left_pointer, D.cs_right, X.non_terminal, PR, NR]
        rhs = [Q_3, PL, C.copied, C.cs_right, X.pointer, PR, C.non_terminal + D.non_terminal + NR]
        P_Q3.append(Rule(lhs, rhs))
    for X in alphabet_extended:
        lhs = [Q_3, PL, X.pointer, PR, NR]
        rhs = [Q_3, PL, X.terminal, PR, X.non_terminal + NR]
        P_Q3.append(Rule(lhs, rhs))
    for C, D in itertools.product(N_extended, N_extended):
        lhs = [Q_3, PL, C.cs_left_pointer, D.cs_right, PR, NR]
        rhs = [Q_3, PL, C.copied, D.cs_right, PR, C.non_terminal + D.non_terminal + NR]
        P_Q3.append(Rule(lhs, rhs))
    for D, X, Y in itertools.product(N_extended, alphabet_extended, alphabet_extended):
        lhs = [Q_3, PL, D.cs_right, X.pointer, Y.non_terminal, PR, NR]
        rhs = [Q_3, PL, D.cs_right, X.terminal, Y.pointer, PR, X.non_terminal + NR]
        P_Q3.append(Rule(lhs, rhs))
    for C, D in itertools.product(N_extended, N_extended):
        lhs = [Q_3, PL, C.copied, D.cs_right, PR]
        rhs = [Q_6, PL, C.terminal, D.terminal, PR]
        P_Q3.append(Rule(lhs, rhs))

    P_Q4 = []
    for symbol in N_extended:
        P_Q4.extend([
            Rule([Q_4, PL, symbol.non_terminal, PR], [Q_5, PL, symbol.pointer, PR]),
            Rule([Q_4, PL, symbol.cs_left, PR], [Q_5, PL, symbol.pointer, PR]),
        ])
    for symbol in T_extended:
        P_Q4.append(
            Rule([Q_4, PL, symbol.non_terminal, PR], [Q_5, PL, symbol.pointer, PR]),
        )

    P_Q5 = []
    for X, Y in itertools.product(alphabet_extended, alphabet_extended):
        lhs = [Q_5, PL, X.pointer, Y.non_terminal, PR, NR]
        rhs = [Q_5, PL, X.terminal, Y.pointer, PR, X.non_terminal + NR]
        P_Q5.append(Rule(lhs, rhs))
    for X in alphabet_extended:
        lhs = [Q_5, PL, X.pointer, PR, NR]
        rhs = [Q_6, PL, X.terminal, PR, X.non_terminal + NR]
        P_Q5.append(Rule(lhs, rhs))

    lhs = [Q_6, PL, PR, NL, NR]
    rhs = [Q_1, T_delim, T_delim, PL, PR + NL + NR]
    P_Q6 = [Rule(lhs, rhs)]

    lhs = [Q_7, PL, PR, NL, NR]
    rhs = [T_delim, T_sep, T_delim, T_delim, T_delim]
    P_Q7 = [Rule(lhs, rhs)]
    for X in T_extended:
        rule = Rule([Q_7, PL, X.non_terminal, PR], [Q_7, PL, X.terminal, PR])
        P_Q7.append(rule)

    P_H = [p_init] + P_Q1 + P_Q2 + P_Q3 + P_Q4 + P_Q5 + P_Q6 + P_Q7

    H = Grammar(N_H, T_H, P_H, S_H)

    return H
