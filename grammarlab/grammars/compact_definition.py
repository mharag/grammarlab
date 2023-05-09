from functools import partial

from grammarlab.core.grammar import grammar_restrictions
from grammarlab.grammars.pc_grammar_system import centralized_pc
from grammarlab.load.code import CodeLoad

# Phrase grammars
RE = CodeLoad.phrase_grammar
CS = CodeLoad.phrase_grammar
CF = CodeLoad.context_free_grammar

# Scattered grammars
SCG = CodeLoad.scattered_context_grammar

# Parallel comunicating grammar systems
PC = CodeLoad.pc_grammar_system
CPC = grammar_restrictions(CodeLoad.pc_grammar_system, centralized_pc)
NPC = partial(CodeLoad.pc_grammar_system, returning=False)
NCPC = grammar_restrictions(NPC, centralized_pc)
