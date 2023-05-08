"""This module contains definitions of all supported grammar types.

Grammar can be defined in two ways:

    - using compact definition
    - using full definition

To use compact definition you need to import grammar type by shortcut.
All shortcuts are defined in :mod:`glab.grammars.compact_definition`.
If you want to use full definition you need to import Grammar by its full name.

Examples:
    Full definition

    >>> from glab.grammars import PhraseGrammar

    Compact definition

    >>> from glab.grammars import RE

"""


from glab.grammars.pc_grammar_system import *
from glab.grammars.phrase_grammar import *
from glab.grammars.scattered_context_grammar import *
from glab.grammars.compact_definition import *