"""This module contains definitions of all supported grammar types.

Grammar can be defined in two ways:

    - using compact definition
    - using full definition

To use compact definition you need to import grammar type by shortcut.
All shortcuts are defined in :mod:`glab.grammars.compact_definition`.
If you want to use full definition you need to import Grammar by its full name.

Examples:
    Full definition

    >>> from grammarlab.grammars import PhraseGrammar

    Compact definition

    >>> from grammarlab.grammars import RE

"""


from grammarlab.grammars.compact_definition import *
from grammarlab.grammars.pc_grammar_system import *
from grammarlab.grammars.phrase_grammar import *
from grammarlab.grammars.scattered_context_grammar import *
