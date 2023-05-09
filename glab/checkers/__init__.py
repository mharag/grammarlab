"""This module contains checkers for checking grammar properties.

Checker can be used to ensure that provided grammar has some properties.

Examples:
    >>> from glab.grammars import CF
    >>> from glab.checkers import chomsky_normal_form
    >>> grammar = CF({"S"}, {"a"}, [("S", "aa"), ("S", "Saa")], "S")
    >>> chomsky_normal_form(grammar)
    False

"""

from glab.checkers.phrase_grammar_normal_forms import *
