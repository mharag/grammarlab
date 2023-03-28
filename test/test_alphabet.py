from glab.alphabet import Symbol, NonTerminal, Terminal, Alphabet, String, N


def test_symbol_eq():
    s1 = Symbol("S")
    s2 = Symbol("S")
    s3 = Symbol("X")
    assert s1 == s2
    assert not s2 == s3


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
        N("A"), N("B"), N("C"), N("D"), N("A")
    ])
    index = str1.create_index()
    assert index[N("A")] == [0, 4]
    assert index[N("B")] == [1]
    assert index[N("C")] == [2]

    selective_index = str1.create_index([N("A")])
    assert len(selective_index) == 1


def test_expand():
    str1 = String([N("A"), N("B"), N("C")])
    str2 = String([N("D"), N("E")])
    str1.expand(1, str2)
    assert str1 == String([N("A"), N("D"), N("E"), N("C")])


def test_replace():
    str1 = String([N("A"), N("B"), N("C")])
    str1.replace(1, N("X"))
    assert str1 == String([N("A"), N("X"), N("C")])


def test_copy():
    str1 = String([N("A"), N("B"), N("C")])
    copied = str1.copy()

    assert str1 == copied
    str1.replace(0, N("D"))
    assert not str1 == copied
