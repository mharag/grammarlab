from glab.alphabet import A, N, S, T


def compact_nonterminal_alphabet(symbols):
    symbols = {N(symbol) for symbol in symbols}
    return A(symbols)


def compact_terminal_alphabet(symbols):
    symbols = {T(symbol) for symbol in symbols}
    return A(symbols)


def compact_communication_symbols(symbols):
    symbols = [N(symbol) for symbol in symbols]
    return symbols


def compact_string(alphabet, string, delimiter=None):
    result = []
    if delimiter:
        string = string.split(delimiter)
    for symbol in string:
        result.append(alphabet.lookup(symbol))
    return S(result)


def compact_rules(rule_class, rules):
    parsed_rules = []
    for lhs, rhs in rules:
        if isinstance(lhs, str):
            lhs = list(lhs)
        if isinstance(rhs, str):
            rhs = list(rhs)
        parsed_rules.append(rule_class(lhs, rhs))
    return parsed_rules
