from tabulate import tabulate

from glab.core.alphabet import String, Symbol
from glab.core.config import RESET, STRING_DELIMITER
from glab.core.extended_symbol import ExtendedSymbol
from glab.core.grammar_base import DerivationSequence
from glab.export.export import Export, formatter
from glab.grammars.pc_grammar_system import (CommunicationRule,
                                             PCConfiguration, PCGrammarSystem)
from glab.grammars.phrase_grammar import (PhraseConfiguration, PhraseGrammar,
                                          PhraseRule)
from glab.grammars.scattered_context_grammar import ScatteredContextRule


def create_table(colums, rows):
    if not rows:
        return ""
    return tabulate(rows, colums, tablefmt="orgtbl")


class CliExport(Export):
    """Export object to command line
    """

    @formatter(Symbol)
    def symbol(self, symbol):
        return symbol.id

    @formatter(ExtendedSymbol)
    def extended_symbol(self, symbol):
        if symbol.color:
            base_len = len(symbol.base_symbol.id)
            base_part = self.export(symbol.base_symbol)
            extended_part = symbol.id[base_len:]
            if extended_part:
                return f"{base_part}{symbol.color}{extended_part}{RESET}"
        return self.export(symbol.base_symbol)

    @formatter(String)
    def string(self, string):
        return STRING_DELIMITER.join(self.export(symbol) for symbol in string)

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

    @formatter(PhraseRule)
    def phrase_rule(self, rule):
        return f"{self.export(rule.lhs)} -> {self.export(rule.rhs)}"

    @formatter(DerivationSequence)
    def derivation_sequence(self, sequence):
        if isinstance(sequence[0], PhraseConfiguration):
            columns = ["Used Rule", "Sential Form"]
            rows = [(self.export(c.used_production), self.export(c.sential_form)) for c in sequence]
        elif isinstance(sequence[0], PCConfiguration):
            columns, rows = [], []
            for i in range(sequence[0].order):
                columns.extend([f"Used Rule {i}", f"Sential Form {i}"])
            for c in sequence:
                row = []
                for i in range(c.order):
                    row.extend(
                        [self.export(c[i].used_production), self.export(c[i].sential_form)]
                    )
                rows.append(row)
        else:
            raise NotImplementedError
        return create_table(columns, rows)

    @formatter(PhraseConfiguration)
    def phrase_configuration(self, configuration):
        return self.export(configuration.sential_form)

    # Scattered context grammars
    @formatter(ScatteredContextRule)
    def scattered_rule(self, rule):
        lhs = ",".join(map(self.export, rule.lhs))
        rhs = ",".join(map(self.export, rule.rhs))
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
        return "  ".join(map(self.export, configuration.data))

    @formatter(CommunicationRule)
    def communication_rule(self, rule):  # pylint: disable=unused-argument
        return "Communication Step"
