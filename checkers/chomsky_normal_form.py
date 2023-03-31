from grammars.phrase_grammar import context_free, PhraseGrammar
from glab.alphabet import NonTerminal, Terminal


def chomsky_normal_form(grammar):
    if not isinstance(grammar, PhraseGrammar):
        return False
    try:
        context_free(grammar)
    except ValueError:
        return False

    for rule in grammar.rules:
        if len(rule.rhs) == 1:
            if type(rule.rhs[0]) != Terminal:
                return False
        elif len(rule.rhs) == 2:
            if type(rule.rhs[0]) != Terminal or type(rule.rhs[1]) != Terminal:
                return False
        else:
            return False

    return True
