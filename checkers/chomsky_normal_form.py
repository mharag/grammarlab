from glab.alphabet import Terminal
from grammars.phrase_grammar import PhraseGrammar, context_free


def chomsky_normal_form(grammar):
    if not isinstance(grammar, PhraseGrammar):
        return False
    try:
        context_free(grammar)
    except ValueError:
        return False

    for rule in grammar.rules:
        if len(rule.rhs) == 1:
            if not isinstance((rule.rhs[0]), Terminal):
                return False
        elif len(rule.rhs) == 2:
            if not isinstance(rule.rhs[0], Terminal) or not isinstance(rule.rhs[1], Terminal):
                return False
        else:
            return False

    return True
