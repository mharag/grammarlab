from grammars.phrase_grammar import context_free, PhraseGrammar
from glab.alphabet import NonTerminal, Terminal
from functools import partial
from itertools import zip_longest, cycle


def match_rule(rule, templates):
    for template in templates:
        matched = True
        for expected_type, symbol in zip_longest(template[0], rule.lhs):
            if type(symbol) != expected_type:
                matched = False
        for expected_type, symbol in zip_longest(template[1], rule.rhs):
            if type(symbol) != expected_type:
                matched = False
        if matched:
            return True
    return False


def match_grammar(templates, grammar):
    if not isinstance(grammar, PhraseGrammar):
        return False
    for rule in grammar.rules:
        if not match_rule(rule, templates):
            return False
    return True


_kuruda_type_1 = [
    ([NonTerminal, NonTerminal], [NonTerminal, NonTerminal]),
    ([NonTerminal], [NonTerminal, NonTerminal]),
    ([NonTerminal], [Terminal]),
]
_kuruda_type_0 = _kuruda_type_1 + [([NonTerminal], [])]
_chomsky_normal_form = [
    ([NonTerminal], [NonTerminal, NonTerminal]),
    ([NonTerminal], [Terminal]),
]

kuruda_normal_form_type_0 = partial(match_grammar, _kuruda_type_0)
kuruda_normal_form_type_1 = partial(match_grammar, _kuruda_type_1)
chomsky_normal_form = partial(match_grammar, _chomsky_normal_form)
