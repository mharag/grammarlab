from functools import partial

from glab.core.grammar_base import restrictions
from glab.grammars.pc_grammar_system import centralized_pc
from glab.load.code import CodeLoad

# Phrase grammars
RE = CodeLoad.phrase_grammar
CS = CodeLoad.phrase_grammar
CF = CodeLoad.context_free_grammar

# Scattered grammars
SCG = CodeLoad.scattered_context_grammar

# Parallel comunicating grammar systems
PC = CodeLoad.pc_grammar_system
CPC = restrictions(CodeLoad.pc_grammar_system, centralized_pc)
NPC = partial(CodeLoad.pc_grammar_system, returning=False)
NCPC = restrictions(NPC, centralized_pc)
