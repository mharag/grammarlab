from tabulate import tabulate

from glab.grammars.pc_grammar_system import PCConfiguration
from glab.grammars.phrase_grammar import PhraseConfiguration, PhraseGrammarRule

definitions = {
    PCConfiguration: lambda obj: [
        (lambda x: x.depth, "Depth"),
        *[(lambda x, i=i: x[i].cli_output(), f"Component {i}") for i in range(obj.order)]
    ],
    PhraseConfiguration: [
        (lambda x: x.used_production, "Used Rule"),
        (lambda x: x.sential_form.cli_output(), "Sential Form"),
    ],

    PhraseGrammarRule: [
        (lambda x: x.label, "Label"),
        (lambda x: x.cli_out(), "Rule"),
    ]
}


def table_supported(obj):
    for key in definitions:
        if isinstance(obj, key):
            return True
    return False


def create_table(rows):
    if not rows:
        return ""

    for key, value in definitions.items():
        if isinstance(rows[0], key):
            columns = value
            break
    else:
        raise ValueError(f"Table does not supper {rows[0].__class__.__name__}!")

    if callable(columns):
        columns = columns(rows[0])

    headers = [column[1] for column in columns]
    table_rows = []
    for row in rows:
        table_rows.append([query(row) for query, _ in columns])

    return tabulate(table_rows, headers, tablefmt="orgtbl")
