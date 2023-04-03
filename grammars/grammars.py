from functools import partial

from glab.grammar_base import restrictions
from grammars.pc_grammar_system import PCGrammarSystem, centralized_pc
from grammars.phrase_grammar import (PhraseGrammar, context_free,
                                     length_preserving)
from grammars.scattered_context_grammar import ScatteredContextGrammar

# Phrase grammars
RE = PhraseGrammar.deserialize
CS = restrictions(PhraseGrammar.deserialize, length_preserving)
CF = restrictions(PhraseGrammar.deserialize, context_free)

# Scattered grammars
SCG = ScatteredContextGrammar.deserialize

# Parallel comunicating grammar systems
PC = PCGrammarSystem.deserialize
CPC = restrictions(PCGrammarSystem.deserialize, centralized_pc)
NPC = partial(PCGrammarSystem.deserialize, returning=False)
NCPC = restrictions(partial(PCGrammarSystem.deserialize, returning=False), centralized_pc)
