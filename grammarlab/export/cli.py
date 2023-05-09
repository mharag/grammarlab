from tabulate import tabulate

from grammarlab.core.common import Alphabet, String, Symbol
from grammarlab.core.config import COLOR_CLI_OUTPUT, STRING_DELIMITER, Color
from grammarlab.core.extended_symbol import ExtendedSymbol
from grammarlab.core.grammar import DerivationSequence
from grammarlab.export.export import Export, formatter
from grammarlab.grammars.pc_grammar_system import (
    CommunicationRule,
    PCConfiguration,
    PCGrammarSystem,
)
from grammarlab.grammars.phrase_grammar import (
    PhraseConfiguration,
    PhraseGrammar,
    PhraseRule,
)
from grammarlab.grammars.scattered_context_grammar import ScatteredContextRule


def _create_table(colums, rows):
    if not rows:
        return ""
    return tabulate(rows, colums, tablefmt="orgtbl")


class CliExport(Export):
    """Export object to command line
    """

    @formatter(str)
    def _str(self, string):
        """helper function to export string"""
        return string

    @formatter(set)
    def _set(self, set_):
        """helper function to export set"""
        return "{" + ", ".join(self.export(item) for item in set_) + "}"

    @formatter(tuple)
    def _tuple(self, tuple_):
        """helper function to export tuple"""
        return "(" + ", ".join(self.export(item) for item in tuple_) + ")"

    @formatter(list)
    def _list(self, list_):
        """helper function to export list"""
        return "[" + ", ".join(self.export(item) for item in list_) + "]"

    @formatter(Symbol)
    def Symbol(self, symbol):
        """
        .. code-block:: text

            S

        """
        return symbol.id

    @formatter(Alphabet)
    def Alphabet(self, alphabet):
        """
        .. code-block:: text

            {S, A, B, C, a, b, c}

        """
        return "{" + str(", ".join(self.export(symbol) for symbol in alphabet)) + "}"

    @formatter(ExtendedSymbol)
    def ExtendedSymbol(self, symbol):
        """
        .. code-block:: text

            S_flag

        """
        if symbol.color and COLOR_CLI_OUTPUT:
            base_len = len(symbol.base_symbol.id)
            base_part = self.export(symbol.base_symbol)
            extended_part = symbol.id[base_len:]
            if extended_part:
                return f"{base_part}{symbol.color}{extended_part}{Color.RESET}"
        return self.export(symbol.base_symbol)

    @formatter(String)
    def String(self, string):
        """
        .. code-block:: text

            A A A A a a a a

        :const:`grammarlab.core.config.STRING_DELIMITER` is used to separate symbols

        """
        return STRING_DELIMITER.join(self.export(symbol) for symbol in string) or "ε"

    # Phrase grammars
    @formatter(PhraseGrammar)
    def PhraseGrammar(self, grammar):
        """
        .. code-block:: text

            PhraseGrammar
            Non-terminals: {S, A, B, C}
            Terminals: {a, b, c}
            Start symbol: S
            Rules:
                  S -> A
                  A -> a A

        """
        rules = "\n".join([f"   {self.export(rule)}" for rule in grammar.rules])
        grammar_template = f"""{grammar.__class__.__name__}
Non-terminals: {self.export(grammar.non_terminals)}
Terminals: {self.export(grammar.terminals)}
Start symbol: {self.export(grammar.start_symbol)}
Rules:
{rules}"""
        return grammar_template

    @formatter(PhraseRule)
    def PhraseRule(self, rule):
        """
        .. code-block:: text

            S -> A

        """
        return f"{self.export(rule.lhs)} -> {self.export(rule.rhs)}"

    @formatter(DerivationSequence)
    def DerivationSequence(self, sequence):
        """
        .. code-block:: text

            | Used Rule   | Sential Form   |
            |-------------|----------------|
            |             | S              |
            | S -> S S    | S S            |
            | S -> ( S )  | ( S ) S        |
            | S -> ( )    | ( ( ) ) S      |
            | S -> ( )    | ( ( ) ) ( )    |


        """
        if isinstance(sequence[0], PhraseConfiguration):
            columns = ["Used Rule", "Sential Form"]
            rows = [(self.export(c.used_rule), self.export(c.sential_form)) for c in sequence]
        elif isinstance(sequence[0], PCConfiguration):
            columns, rows = [], []
            for i in range(sequence[0].order):
                columns.extend([f"Used Rule {i}", f"Sential Form {i}"])
            for c in sequence:
                row = []
                for i in range(c.order):
                    row.extend(
                        [self.export(c[i].used_rule), self.export(c[i].sential_form)]
                    )
                rows.append(row)
        else:
            raise NotImplementedError
        return _create_table(columns, rows)

    @formatter(PhraseConfiguration)
    def PhraseConfiguration(self, configuration):
        """
        .. code-block:: text

            ( S ) S

        :const:`grammarlab.core.config.STRING_DELIMITER` is used to separate symbols

        """
        return self.export(configuration.sential_form)

    # Scattered context grammars
    @formatter(ScatteredContextRule)
    def ScatteredContextRule(self, rule):
        """
        .. code-block:: text

            (S, A) -> (A, S)

        """
        lhs = ",".join(map(self.export, rule.lhs))
        rhs = ",".join(map(self.export, rule.rhs))
        return f"({lhs}) -> ({rhs})"

    # Parallel communicating grammar systems
    @formatter(PCGrammarSystem)
    def PCGrammarSystem(self, grammar):
        """
        .. code-block:: text

            PCGrammarSystem
            Communication symbols: [1, 2]

            Component 1: PhraseGrammar
            ...

            Component 2: PhraseGrammar
            ...

        """
        components = "\n\n".join([
            f"Component {i}: {self.export(component)}" for i, component in enumerate(grammar.components)
        ])
        communication_symbols = ", ".join(map(self.export, grammar.communication_symbols))
        grammar_template = f"""{grammar.__class__.__name__}
Communication symbols: [{communication_symbols}]

{components}
"""
        return grammar_template

    @formatter(PCConfiguration)
    def PCConfiguration(self, configuration):
        """
        .. code-block:: text

            a a  b b  c c

        :const:`grammarlab.core.config.STRING_DELIMITER` is used to separate symbols.
        Components are separated by two STRING_DELIMITERs.

        """
        return "\t\t".join(map(self.export, configuration.data))

    @formatter(CommunicationRule)
    def CommunicationRule(self, rule):  # pylint: disable=unused-argument
        """
        .. code-block:: text

            Communication Step

        """
        return "Communication Step"
