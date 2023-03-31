from grammars.scattered_context_grammar import ScatteredContextGrammar
from grammars.phrase_grammar import PhraseGrammar, context_free, length_preserving
from glab.grammar_base import restrictions
from grammars.pc_grammar_system import PCGrammarSystem, centralized
from functools import partial


# Phrase grammars
RE = PhraseGrammar.construct
CS = restrictions(PhraseGrammar.construct, length_preserving)
CF = restrictions(PhraseGrammar.construct, context_free)

# Scattered grammars
SCG = ScatteredContextGrammar.construct

# Parallel comunicating grammar systems
PC = PCGrammarSystem.construct
CPC = restrictions(PCGrammarSystem.construct, centralized)
NPC = partial(PCGrammarSystem.construct, returning=False)
NCPC = restrictions(partial(PCGrammarSystem.construct, returning=False), centralized)
