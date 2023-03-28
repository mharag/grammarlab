from grammar.scattered_context_grammar import ScatteredContextGrammar
from grammar.output import Output
from grammar.phrase_grammar import PhraseGrammar


def construct_grammar(grammar_class):
    def constructor(*args, **kwargs):
        grammar = grammar_class.construct(*args, **kwargs)
        return Output(grammar)

    return constructor


SCG = construct_grammar(ScatteredContextGrammar)
CS = construct_grammar(PhraseGrammar)
