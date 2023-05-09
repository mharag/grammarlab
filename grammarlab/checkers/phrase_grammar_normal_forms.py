from functools import partial
from typing import List

from grammarlab.core.common import SymbolType
from grammarlab.grammars.phrase_grammar import PhraseGrammar


def match_rule(rule, templates):
    """Check if rule matches at least one template.

    template can be explicit tuple of lists of types
    or function that takes rule as argument and returns True if rule matches template.

    Args:
        rule: PhraseRule to check
        templates: list of templates to match against

    Returns:
        True if rule matches at least one template, False otherwise

    """
    for template in templates:
        if callable(template):
            matched = template(rule)
        else:
            matched = True
            for actual_string, expected_string in [(rule.lhs, template[0]), (rule.rhs, template[1])]:
                if len(actual_string) != len(expected_string):
                    matched = False
                    break
                for expected_type, actual_symbol in zip(expected_string, actual_string):
                    if not actual_symbol.type == expected_type:
                        matched = False
        if matched:
            return True
    return False


def match_grammar(templates: List, grammar: PhraseGrammar):
    """Check if every rule in grammar matches at least one template.

    Args:
        templates: list of templates to match against
        grammar: PhraseGrammar to check

    Returns:
        True if every rule in grammar matches at least one template, False otherwise

    """
    if not isinstance(grammar, PhraseGrammar):
        return False
    for rule in grammar.rules:
        if not match_rule(rule, templates):
            return False
    return True


NonTerminal = SymbolType.NON_TERMINAL
Terminal = SymbolType.TERMINAL

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
_greibach_normal_form = [
    lambda x: (
        len(x.lhs) == 1 and x.rhs[0].type == Terminal and all(s.type == NonTerminal for s in x.rhs[1:])
    ),
]

kuruda_normal_form_type_0 = partial(match_grammar, _kuruda_type_0)
"""Returns True if every rule of grammar is one of the following forms:

    - :math:`AB \\rightarrow CD`
    - :math:`A \\rightarrow BC`
    - :math:`A \\rightarrow a`
    - :math:`A \\rightarrow \\epsilon`

"""
kuruda_normal_form_type_1 = partial(match_grammar, _kuruda_type_1)
"""Returns True if every rule of grammar is one of the following forms:

    - :math:`AB \\rightarrow CD`
    - :math:`A \\rightarrow BC`
    - :math:`A \\rightarrow a`

"""
chomsky_normal_form = partial(match_grammar, _chomsky_normal_form)
"""Returns True if every rule of grammar is one of the following forms:

    - :math:`A \\rightarrow BC`
    - :math:`A \\rightarrow a`

"""
greibach_normal_form = partial(match_grammar, _greibach_normal_form)
"""Returns True if every rule of grammar is one of the following forms:

    - :math:`A \\rightarrow aB_1B_2\\dots B_n`
    - :math:`A \\rightarrow a`

"""
