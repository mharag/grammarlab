from glab.core.config import STRING_DELIMITER
from glab.examples.kuruda_normal_form import grammar
from glab.transformations.pcgs_pscg_re_equivalence import construct_grammar


def test_transformation():
    new_grammar = construct_grammar(grammar)
    result = new_grammar.derive(50)
    result = set(map(lambda x: str(x.sential_form), result))
    expected = {"a", f"a{STRING_DELIMITER}a"}
    assert result == expected
