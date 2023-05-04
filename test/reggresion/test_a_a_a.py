from glab.core.cli import App
from glab.core.config import STRING_DELIMITER
from glab.languages.cs_aaa import grammar


def test_a_a_a(capsys):
    expected = ["a_a_a",
        "aa_aa_aa",
        "aaa_aaa_aaa",
        "aaaa_aaaa_aaaa",
        "aaaaa_aaaaa_aaaaa",
        "aaaaaa_aaaaaa_aaaaaa",
    ]
    expected = [STRING_DELIMITER.join(x) for x in expected]
    expected = "\n".join(expected) + "\n"

    App(grammar).generate(50)
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == expected
