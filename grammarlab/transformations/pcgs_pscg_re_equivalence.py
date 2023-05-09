from grammarlab.transformations.accept_substring import (
    construct_grammar as accept_substring,
)
from grammarlab.transformations.derivation_sequence_in_scg import (
    construct_grammar as derivation_sequence_in_scg,
)


def construct_grammar(grammar):
    derivation_sequence_grammar = derivation_sequence_in_scg(grammar)
    return accept_substring(derivation_sequence_grammar, "#")
