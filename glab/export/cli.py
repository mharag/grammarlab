from tabulate import tabulate

from glab.export.export import Export, formatter
from glab.grammars.pc_grammar_system import PCConfiguration, PCGrammarSystem
from glab.grammars.phrase_grammar import (PhraseConfiguration, PhraseGrammar,
                                          PhraseGrammarRule)
from glab.grammars.scattered_context_grammar import ScatteredContextRule


def create_table(colums, rows):
    if not rows:
        return ""
    return tabulate(rows, colums, tablefmt="orgtbl")


class CliExport(Export):
    """Export object to command line
    """

    # Phrase grammars
    @formatter(PhraseGrammar)
    def phrase_grammar(self, grammar):
        rules = "\n".join([f"   {self.export(rule)}" for rule in grammar.rules])
        grammar_template = f"""{grammar.__class__.__name__}
Non-terminals: {str(grammar.non_terminals)}
Terminals: {str(grammar.terminals)}
Start symbol: {str(grammar.start_symbol)}
Rules:
{rules}"""
        return grammar_template

    @formatter(PhraseGrammarRule)
    def phrase_rule(self, rule):
        lhs = " ".join(map(str, rule.lhs))
        rhs = " ".join(map(str, rule.rhs))
        return f"{lhs} -> {rhs}"

    @formatter(PhraseConfiguration)
    def phrase_configuration(self, configuration):
        columns = ["Used Rule", "Sential Form"]
        rows = [(c.used_production, c.sential_form) for c in configuration.derivation_sequence()]
        return create_table(columns, rows)

    # Scattered context grammars
    @formatter(ScatteredContextRule)
    def scattered_rule(self, rule):
        lhs = ",".join(map(str, rule.lhs))
        rhs = ",".join(map(str, rule.rhs))
        return f"({lhs}) -> ({rhs})"

    # Parallel communicating grammar systems
    @formatter(PCGrammarSystem)
    def pc_grammar_system(self, grammar):
        components = "\n\n".join([
            f"Component {i}: {self.export(component)}" for i, component in enumerate(grammar.components)
        ])
        grammar_template = f"""{grammar.__class__.__name__}
Communication symbols: {str(grammar.communication_symbols)}

{components}
"""
        return grammar_template

    @formatter(PCConfiguration)
    def pc_configuration(self, configuration):
        columns, rows = [], []
        for i in range(configuration.order):
            columns.extend([f"Used Rule {i}", f"Sential Form {i}"])
        for c in configuration.derivation_sequence():
            row = []
            for i in range(configuration.order):
                row.extend(
                    [c[i].used_production or "", c[i].sential_form]
                )
            rows.append(row)
        return create_table(columns, rows)
