from grammars.scattered_context_grammar import ScatteredContextGrammar
from grammars.phrase_grammar import PhraseGrammar, context_free, length_preserving
from glab.grammar_base import restrictions


SCG = ScatteredContextGrammar.construct
RE = PhraseGrammar.construct
CS = restrictions(PhraseGrammar.construct, length_preserving)
CF = restrictions(PhraseGrammar.construct, context_free)
