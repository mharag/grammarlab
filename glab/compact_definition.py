from glab.alphabet import S, N, T, A


def compact_nonterminal_alphabet(symbols):
    symbols = {N(symbol) for symbol in symbols}
    return A(symbols)


def compact_terminal_alphabet(symbols):
    symbols = {T(symbol) for symbol in symbols}
    return A(symbols)


def compact_communication_symbols(symbols):
    symbols = [N(symbol) for symbol in symbols]
    return symbols


def compact_string(alphabet, string):
    result = []
    for symbol in string:
        result.append(alphabet.lookup(symbol))
    return S(result)


def compact_rules(rule_class, rules):
    parsed_rules = []
    for lhs, rhs in rules:
        if type(lhs) == str:
            lhs = list(lhs)
        if type(rhs) == str:
            rhs = list(rhs)
        parsed_rules.append(rule_class(lhs, rhs))
    return parsed_rules



