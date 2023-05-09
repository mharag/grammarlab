from grammarlab.core.app import App
from grammarlab.core.config import STRING_DELIMITER
from grammarlab.examples.cs_aaa import grammar


def format_expected_result(expected):
    expected = [STRING_DELIMITER.join(x) for x in expected]
    expected = "\n".join(expected) + "\n"
    return expected


def test_generate(capsys):
    expected = format_expected_result(["a_a_a",
        "aa_aa_aa",
        "aaa_aaa_aaa",
        "aaaa_aaaa_aaaa",
        "aaaaa_aaaaa_aaaaa",
        "aaaaaa_aaaaaa_aaaaaa",
    ])

    App(grammar).generate(50)
    captured = capsys.readouterr()
    assert captured.out == expected


def test_generate_exact_depth(capsys):
    expected = format_expected_result(["aaa_aaa_aaa"])

    App(grammar).generate(11, exact_depth=True)
    captured = capsys.readouterr()
    assert captured.out == expected


def test_generate_sential_form(capsys):
    expected = format_expected_result([
        "a-L-a",
        "a-F_a",
        "aa-AR-a"
    ])

    App(grammar).generate(2, only_sentences=False)
    captured = capsys.readouterr()
    assert captured.out == expected


def test_generate_start(capsys):
    expected = format_expected_result(["a_a_a"])

    App(grammar).generate(1, axiom="a_a-F")
    captured = capsys.readouterr()
    assert captured.out == expected
