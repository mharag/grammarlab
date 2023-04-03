from functools import partial

from glab.grammar_base import restrictions
from grammars.pc_grammar_system import PCGrammarSystem, centralized_pc
from grammars.phrase_grammar import (PhraseGrammar, context_free,
                                     length_preserving)
from grammars.scattered_context_grammar import ScatteredContextGrammar

# Phrase grammars
RE = PhraseGrammar.construct
CS = restrictions(PhraseGrammar.construct, length_preserving)
CF = restrictions(PhraseGrammar.construct, context_free)

# Scattered grammars
SCG = ScatteredContextGrammar.construct

# Parallel comunicating grammar systems
PC = PCGrammarSystem.construct
CPC = restrictions(PCGrammarSystem.construct, centralized_pc)
NPC = partial(PCGrammarSystem.construct, returning=False)
NCPC = restrictions(partial(PCGrammarSystem.construct, returning=False), centralized_pc)
