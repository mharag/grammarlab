from grammarlab.core.common import Alphabet, NonTerminal, String, Terminal


def test_symbol_eq():
    s1 = NonTerminal("S")
    s2 = NonTerminal("S")
    s3 = NonTerminal("X")
    assert s1 == s2
    assert not s2 == s3
    assert s1 is s2
    assert s2 is not s3


def test_symbol_type():
    s1 = Terminal("S")
    s2 = NonTerminal("S")
    assert not s1 == s2


def test_alphabet_contains():
    alph = Alphabet({Terminal("S"), Terminal("N")})
    assert Terminal("S") in alph
    assert Terminal("X") not in alph


def test_alphabet_union():
    alph1 = Alphabet({Terminal("S"), Terminal("N")})
    alph2 = Alphabet({Terminal("S"), Terminal("X")})
    alph3 = Alphabet({Terminal("X"), Terminal("Y")})
    assert len(alph1.union(alph2)) == 3
    assert len(alph1.union(alph3)) == 4


def test_string_is_sentence():
    str1 = String([Terminal("S"), Terminal("X")])
    str2 = String([Terminal("S"), NonTerminal("X")])
    assert str1.is_sentence
    assert not str2.is_sentence


def test_string_create_index():
    str1 = String([
        NonTerminal("A"), NonTerminal("B"), NonTerminal("C"), NonTerminal("D"), NonTerminal("A")
    ])
    index = str1.index
    assert index[NonTerminal("A")] == [0, 4]
    assert index[NonTerminal("B")] == [1]
    assert index[NonTerminal("C")] == [2]


def test_expand():
    str1 = String([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")])
    str2 = String([NonTerminal("D"), NonTerminal("E")])
    str1.expand(1, str2)
    assert str1 == String([NonTerminal("A"), NonTerminal("D"), NonTerminal("E"), NonTerminal("C")])


def test_replace():
    str1 = String([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")])
    str1.replace(1, NonTerminal("X"))
    assert str1 == String([NonTerminal("A"), NonTerminal("X"), NonTerminal("C")])


def test_copy():
    str1 = String([NonTerminal("A"), NonTerminal("B"), NonTerminal("C")])
    copied = str1.copy()

    assert str1 == copied
    str1.replace(0, NonTerminal("D"))
    assert not str1 == copied
