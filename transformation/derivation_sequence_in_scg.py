from grammars.scattered_context_grammar import ScatteredContextRule as Rule, ScatteredContextGrammar as Grammar
from glab.alphabet import S,N,T,Alphabet
from glab.compact_definition import compact_string, compact_nonterminal_alphabet
import itertools
from glab.cli import App


def f(symbol):
    txt = symbol.symbol
    if txt[-2:] in ["_O", "_T", "_<", "_>"]:
        return T(txt[:-2])
    if txt[-2:] in ["^+"]:
        return T(txt[:-4])
    raise ValueError(f"Unknown symbol: {symbol}")



def construct_grammar(G):
    print(G)
    N_G = G.non_terminals
    T_G = G.terminals
    P_G = G.rules
    S_G = G.start_symbol

    S_O = N(f"{S_G.symbol}_O")
    S_H = N("S_H")
    N_O = {N(f"{symbol}_O") for symbol in N_G}
    N_T = {N(f"{symbol}_T") for symbol in T_G}
    Q_1, Q_2, Q_3, Q_4, Q_5, Q_6, Q_7 = N("Q_1"), N("Q_2"), N("Q_3"), N("Q_4"), N("Q_5"), N("Q_6"), N("Q_7")
    Q = {Q_1, Q_2, Q_3, Q_4, Q_5, Q_6}
    PL, PR, NL, NR = N("["), N("]"), N("<"), N(">")
    K = {PL, PR, NL, NR}
    N_langle = {N(f"{symbol}_<") for symbol in N_G}
    N_rangle = {N(f"{symbol}_>") for symbol in N_G}
    N_actual = {N(f"{symbol}^*") for symbol in N_O | N_langle | N_rangle}
    N_copied = {N(f"{symbol}^+") for symbol in N_langle | N_rangle}
    N_H = Alphabet({S_H} | N_O | N_T | Q | K | N_langle | N_rangle | N_actual | N_copied)

    T_O = {T(f"{symbol}_O") for symbol in T_G}
    T_N = {T(f"{symbol}_N") for symbol in N_G}
    T_e = T("e")
    T_delim = T("*")
    T_H = Alphabet(T_O | T_N | {T_e, T_delim})

    p_init = Rule([S_H], [Q_1 + PL + S_O + PR + NL + NR])

    P_Q1 = [Rule([Q_1], [Q_7])]
    for rule in P_G:
        if len(rule.lhs) == 2 and len(rule.rhs) == 2:
            A, B = rule.lhs
            C, D = rule.rhs
            lhs = [Q_1, PL, N(f"{A}_O"), N(f"{B}_O"), PR]
            rhs = [Q_2, PL, N(f"{C}_<"), N(f"{D}_>"), PR]
            P_Q1.append(Rule(lhs, rhs))
        elif len(rule.lhs) == 1 and len(rule.rhs) == 2:
            A = rule.lhs[0]
            B, C = rule.rhs
            lhs = [Q_1, PL, N(f"{A}_O"), PR]
            rhs = [Q_4, PL, N(f"{B}_O") + N(f"{C}_O"), PR]
            P_Q1.append(Rule(lhs, rhs))
        elif len(rule.lhs) == 1 and len(rule.rhs) == 1:
            A = rule.lhs[0]
            B = rule.rhs[0]
            lhs = [Q_1, PL, N(f"{A}_O"), PR]
            rhs = [Q_4, PL, N(f"{B}_T"), PR]
            P_Q1.append(Rule(lhs, rhs))
        elif len(rule.lhs) == 1 and len(rule.rhs) == 0:
            A = rule.lhs[0]
            lhs = [Q_1, PL, N(f"{A}_O"), PR]
            rhs = [Q_4, PL, T_e, PR]
            P_Q1.append(Rule(lhs, rhs))

    P_Q2 = []
    for symbol in N_O | N_T | N_langle:
        rule = Rule([Q_2, PL, symbol, PR], [Q_3, PL, N(f"{symbol}^*"), PR])
        P_Q2.append(rule)

    P_Q3 = []
    for X, Y, C in itertools.product(N_O | N_T, N_O | N_T, N_langle):
        lhs = [Q_3, PL, N(f"{X}^*"), Y, C, PR, NR]
        rhs = [Q_3, PL, f(X), N(f"{Y}^*"), C, PR, X + NR]
        P_Q3.append(Rule(lhs, rhs))
    for X, C in itertools.product(N_O | N_T, N_langle):
        lhs = [Q_3, PL, N(f"{X}^*"), C, PR, NR]
        rhs = [Q_3, PL, f(X), N(f"{C}^*"), PR, X + NR]
        P_Q3.append(Rule(lhs, rhs))
    for C, D, X in itertools.product(N_langle, N_rangle, N_O | N_T):
        lhs = [Q_3, PL, N(f"{C}^*"), D, X, PR, NR]
        rhs = [Q_3, PL, N(f"{C}^+"), N(f"{D}^+"), N(f"{X}^*"), PR, C + D + NR]
        P_Q3.append(Rule(lhs, rhs))
    for X in N_O | N_T:
        lhs = [Q_3, PL, N(f"{X}^*"), PR, NR]
        rhs = [Q_3, PL, f(X), PR, X + NR]
        P_Q3.append(Rule(lhs, rhs))
    for C, D, X in itertools.product(N_langle, N_rangle, N_O | N_T):
        lhs = [Q_3, PL, N(f"{C}^*"), D, PR, NR]
        rhs = [Q_3, PL, N(f"{C}^+"), N(f"{D}^+"), PR, C + D + NR]
        P_Q3.append(Rule(lhs, rhs))
    for D, X, Y in itertools.product(N_rangle, N_O | N_T, N_O | N_T):
        lhs = [Q_3, PL, N(f"{D}^+"), N(f"{X}^*"), Y, PR, NR]
        rhs = [Q_3, PL, N(f"{D}^+"), f(X), N(f"{Y}^*"), PR, X + NR]
        P_Q3.append(Rule(lhs, rhs))
    for C, D, X in itertools.product(N_langle, N_rangle, N_O | N_T):
        lhs = [Q_3, PL, N(f"{C}^+"), N(f"{D}^+"), PR]
        rhs = [Q_6, PL, f(C), f(D), PR]
        P_Q3.append(Rule(lhs, rhs))

    P_Q4 = []
    for symbol in N_O | N_T:
        rule = Rule([Q_4, PL, symbol, PR], [Q_5, PL, N(f"{symbol}^*"), PR])
        P_Q4.append(rule)

    P_Q5 = []
    for X, Y in itertools.product(N_O | N_T, N_O | N_T):
        lhs = [Q_5, PL, N(f"{X}^*"), Y, PR, NR]
        rhs = [Q_5, PL, f(X), N(f"{Y}^*"), PR, X + NR]
        P_Q5.append(Rule(lhs, rhs))
    for X in N_O | N_T:
        lhs = [Q_5, PL, N(f"{X}^*"), PR, NR]
        rhs = [Q_6, PL, f(X), PR, X + NR]
        P_Q5.append(Rule(lhs, rhs))

    lhs = [Q_6, PL, PR, NL, NR]
    rhs = [Q_1, T_delim, T_delim, PL, PR + NL + NR]
    P_Q6 = [Rule(lhs, rhs)]

    lhs = [Q_7, PL, PR, NL, NR]
    rhs = [T_delim, T_delim, T_delim, T_delim, T_delim]
    P_Q7 = [Rule(lhs, rhs)]
    for X in N_T:
        rule = Rule([Q_7, PL, X, PR], [Q_7, PL, f(X), PR])
        P_Q7.append(rule)

    P_H = [p_init] + P_Q1 + P_Q2 + P_Q3 + P_Q4 + P_Q5 + P_Q6 + P_Q7

    H = Grammar(N_H, T_H, P_H, S_H)

    return H