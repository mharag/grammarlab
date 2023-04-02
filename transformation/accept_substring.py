from grammars.pc_grammar_system import PCGrammarSystem
from glab.alphabet import String, SymbolType, Alphabet
from glab.extended_symbol import ExtendedSymbol, Terminal as T, NonTerminal as N
from grammars.scattered_context_grammar import ScatteredContextGrammar as Grammar, ScatteredContextRule as Rule
import itertools
from glab.config import RED
from glab.filter import grammar_filter


class PCSymbol(ExtendedSymbol):
    color = RED
    variants = {
        "communication": (SymbolType.NON_TERMINAL, "C"),
        "end": (SymbolType.NON_TERMINAL, "E"),
        "pointer": (SymbolType.NON_TERMINAL, "C"),
        "terminal": (SymbolType.TERMINAL, "T"),
        "non_terminal": (SymbolType.NON_TERMINAL, "N"),
    }

    @property
    def terminal(self):
        if self.type == SymbolType.TERMINAL:
            return PCSymbol(self.base_symbol, "terminal", *self.base)
        return PCSymbol(self.base_symbol, "terminal", SymbolType.TERMINAL, "T")


def construct_grammar(G, separator, apply_filters=True):
    N_G = G.non_terminals
    T_G = G.terminals
    P_G = G.rules
    S_G = G.start_symbol
    N_extended = {PCSymbol(x) for x in N_G}
    T_extended = {PCSymbol(x) for x in T_G}
    alphabet_extended = N_extended | T_extended
    N_communication = {x.communication for x in T_extended}
    N_end = {x.end for x in T_extended}
    N_pointer = {x.pointer for x in T_extended}
    T_original = {x.terminal for x in alphabet_extended}
    N_original = {x.non_terminal for x in alphabet_extended}

    S_O = PCSymbol(S_G)
    separator = PCSymbol(T(separator))

    W = N("W")
    E = T("-")

    Q_A = N("Q_A")
    Q_B = N("Q_B")
    Q_C = N("Q_C")
    K = [Q_A, Q_B, Q_C]

    S_C = N("S_C")
    P_C = [
        Rule([S_C], [W])
    ]
    for symbol in T_extended:
        P_C.extend([
            Rule([S_C], [symbol.communication]),
            Rule([symbol.communication], [symbol.communication]),
            Rule([S_C], [symbol.end]),
            Rule([symbol.end], [symbol.end]),
        ])

    C = Grammar(Alphabet(N_communication | N_end | {S_C, W}), Alphabet(set()), P_C, S_C)

    S_A = N("S_A")
    P_A = [
        Rule([S_A], [Q_C]),
        Rule([W], [W]),
    ]
    for symbol in T_extended:
        P_A.extend([
            Rule([symbol.communication], [symbol.terminal + Q_C]),
            Rule([symbol.end], [symbol.non_terminal]),
            Rule([symbol.non_terminal], [symbol.terminal]),
        ])

    A = Grammar(Alphabet(N_communication | N_end | {S_A, W} | N_original), Alphabet(T_original), P_A, S_A)

    S_B = N("S_B")
    R_0, R_1, R_2, R_3 = N("R_0"), N("R_1"), N("R_2"), N("R_3")
    R = {R_0, R_1, R_2, R_3}
    P_B = [
        Rule([S_B], [R_0 + Q_C]),
        Rule([R_0, W], [R_1, S_O.non_terminal]),
        Rule([R_1, separator.non_terminal], [R_2, separator.non_terminal]),
        Rule([R_2], [R_3 + Q_A])
    ]
    ignore = [T("*")]
    for rule in P_G:
        P_B.append(
            Rule(
                [R_1] + [PCSymbol(x).non_terminal for x in rule.lhs],
                [R_1] + [
                    String(
                        [
                            PCSymbol(x).non_terminal if x not in ignore else PCSymbol(x).terminal
                            for x in string
                        ]
                    )
                    for string in rule.rhs
                ],
            )
        )

    for symbol in T_extended:
        P_B.extend([
            Rule(
                [R_2, symbol.non_terminal, separator.non_terminal],
                [R_2, symbol.terminal, separator.non_terminal]
            ),
            Rule(
                [R_3, W, separator.non_terminal, symbol.non_terminal],
                [R_3, Q_C, separator.terminal, symbol.pointer],
            ),
            Rule(
                [R_3, symbol.end, symbol.pointer],
                [E, E, E]
            )
        ])

    for X, Y in itertools.product(T_extended, T_extended):
        P_B.append(
            Rule(
                [R_3, X.communication, X.pointer, Y.non_terminal],
                [R_3, Q_C, X.terminal, Y.pointer]
            )
        )

    B = Grammar(
        Alphabet(N_communication | N_end | N_pointer | N_original | {S_B, W, E} | set(K) | R),
        Alphabet(T_original),
        P_B,
        S_B
    )

    grammar = PCGrammarSystem(K, [A, B, C])
    if apply_filters:
        grammar.set_filter(copy_after_finish)
        grammar.set_filter(finish_part_before_separator)
        grammar.set_filter(finish_from_left_to_right)
        for origin_filter in G.filters:
            grammar.set_filter(translate_to_origin(origin_filter))

    return grammar


def translate_to_origin(origin_filter):
    def wrapper(configuration):
        sential_form = configuration[1]
        if sential_form.sential_form[0] != N("R_1"):
            return True
        new_configuration = sential_form.copy()
        new_configuration.data = [symbol.base_symbol for symbol in sential_form.sential_form[1:]]
        return origin_filter(new_configuration)
    return wrapper


@grammar_filter
def copy_after_finish(configuration):
    B = configuration[1].sential_form
    if B[0] == N("R_2"):
        for symbol in B[1:]:
            if symbol.variant is not None and symbol.base_symbol.variant == "non_terminal":
                return False
    return True


@grammar_filter
def finish_from_left_to_right(configuration):
    B = configuration[1].sential_form
    if B[0] == N("R_2"):
        non_terminal = False
        for symbol in B[1:]:
            if symbol.type == SymbolType.NON_TERMINAL:
                non_terminal = True
            if symbol.variant == SymbolType.TERMINAL:
                if non_terminal:
                    return False
    return True


@grammar_filter
def finish_part_before_separator(configuration):
    B = configuration[1].sential_form
    if B[0] == N("R_3") and B[1] == N("Q_A"):
        for symbol in B[2:]:
            if str(symbol.base_symbol) == "#":
                return True
            if symbol.variant == "non_terminal":
                return False
    return True
