from typing import Dict, Iterable, List, Set, Tuple

from glab.core.alphabet import NonTerminal, String, Symbol, SymbolType
from glab.core.ast import Tree
from glab.core.compact_definition import (compact_nonterminal_alphabet,
                                          compact_string,
                                          compact_terminal_alphabet)
from glab.grammars.phrase_grammar import (PhraseConfiguration, PhraseGrammar,
                                          PhraseGrammarRule)


class SCGConfiguration(PhraseConfiguration):
    """Configuration for the scattered context grammar."""
    def cli_output(self):
        return self.sential_form.cli_output()

    def apply_rule_to_ast(self, parent_ast: Tree, depth=0):
        """Apply the rule to the AST and return the new AST.

        Tree root is same as for PhraseConfiguration.

        """
        lhs_nodes = []
        for position in self.affected:
            lhs_nodes.append(parent_ast.frontier[position])

        for i, string in enumerate(self.used_production.rhs):
            children = [parent_ast.create_node(x, depth) for x in string]
            lhs_nodes[i].add_children(children)
        return parent_ast

    def __str__(self):
        return str(self.data)


class ScatteredContextRule(PhraseGrammarRule):
    """Scattered context rule."""
    index = 0

    def __init__(self, lhs: List[NonTerminal], rhs: List[String]):
        if len(lhs) != len(rhs):
            raise ValueError("Different order of right and left side!")
        if not all(symbol.type == SymbolType.NON_TERMINAL for symbol in lhs):
            raise ValueError("Terminal symbol in left side of rule!")

        self.lhs = lhs

        unified_rhs = []
        for item in rhs:
            if isinstance(item, Symbol):
                item = String([item])
            unified_rhs.append(item)
        self.rhs = unified_rhs

        ScatteredContextRule.index += 1
        self.label = f"p{self.index}"

    @classmethod
    def deserialize(cls, alphabet, rule: Tuple[Iterable, Iterable]):
        """Deserialize rule.

        Serialized rule is tuple containing left and right side.
        Left side is represented as list of symbols.
        Right side is represented as list of strings.

        Examples of serialized rules:
            (["A", "B"], ["CD", "EF"]), ("AB", ["C", "DEF"])

        """
        lhs, rhs = rule
        lhs = [alphabet.lookup(symbol) for symbol in lhs]
        rhs = [compact_string(alphabet, string) for string in rhs]
        return cls(lhs, rhs)

    def __repr__(self):
        lhs = ", ".join(str(symbol) for symbol in self.lhs)
        rhs = ", ".join(str(string) for string in self.rhs)
        return f"{self.label}: ({lhs}) -> ({rhs})"

    @property
    def order(self):
        """Order of rule is number of symbols on left side."""
        return len(self.lhs)

    @staticmethod
    def find_next(
        index: Dict[NonTerminal, List[int]],
        string_position: int,
        last: int,
        symbol: NonTerminal
    ):
        """Find next usable match of symbol in string.

        Args:
            index: Dict where key is symbol and value is list of positions of symbol in string.
            string_position: Position of last used symbol in string. Only symbol after this position can be used.
            last: Position of last used symbol in index. Symbols before last are already used.
            symbol: Symbol we are trying to match.
        Returns
            Position of next usable match of symbol in string or -1 if there is no such match.

        """
        start = 0 if last == -1 else last + 1
        for i in range(start, len(index[symbol])):
            if index[symbol][i] > string_position:
                return i
        return -1

    def match(self, string: String):
        """Find all matches of rule in string."""

        index = string.index
        index_positions = [-1] * self.order

        # cursor is index of symbol on left side which is currently processed
        cursor = 0
        while cursor >= 0:
            # if all symbols on left side are processed, yield match
            if cursor >= self.order:
                yield [index[self.lhs[i]][index_positions[i]] for i in range(self.order)]
                cursor -= 1

            # string position is position of last used symbol in string
            # symbol can be matched only if it is after last matched symbol
            # if cursor is 0, there is no last used symbol
            string_position = -1 if cursor == 0 else index[self.lhs[cursor-1]][index_positions[cursor-1]]

            # symbol we are trying to match
            symbol = self.lhs[cursor]
            # find next usable match in string
            next_position = self.find_next(index, string_position, index_positions[cursor], symbol)
            if next_position == -1:
                # cannot find any other match for symbol
                index_positions[cursor] = -1
                # return to previous symbol in lhs
                cursor -= 1
            else:
                # symbol matched
                index_positions[cursor] = next_position
                # move to next symbol in lhs
                cursor += 1

    def apply(self, configuration: SCGConfiguration):
        """Apply rule to configuration.

        Args:
            configuration: Configuration to which rule is applied.
        Returns:
            Generator of new configurations.

        """
        sential_form = configuration.sential_form
        matches = self.match(sential_form)
        for match in matches:
            derived = sential_form.copy()
            offset = 0
            for cursor in range(self.order):
                derived.expand(match[cursor]+offset, self.rhs[cursor])
                # if we insert string of length n, all positions after it are shifted by n-1
                offset += len(self.rhs[cursor]) - 1
            new_configuration = SCGConfiguration(
                derived,
                parent=configuration,
                used_production=self,
                affected=match,
                depth=configuration.depth + 1
            )
            yield new_configuration


class ScatteredContextGrammar(PhraseGrammar):
    """Scattered context grammar."""
    configuration_class = SCGConfiguration
    production_class = ScatteredContextRule

    @classmethod
    def deserialize(cls, non_terminals: Set, terminals: Set, rules: List, start_symbol: str):
        """Deserialize grammar.

        Args:
            non_terminals: Set of non-terminal symbols represented by str.
            terminals: Set of non-terminal symbols represented by str.
            rules: List of rules. Each rule is tuple containing left and right side.
            start_symbol: Start symbol represented by str.
        Returns:
            Scattered context grammar.

        """
        non_terminals = compact_nonterminal_alphabet(non_terminals)
        terminals = compact_terminal_alphabet(terminals)
        alphabet = non_terminals.union(terminals)
        rules = [ScatteredContextRule.deserialize(alphabet, rule) for rule in rules]
        start_symbol = NonTerminal(start_symbol)
        return cls(non_terminals, terminals, rules, start_symbol)

    @property
    def axiom(self):
        """Axiom of grammar is configuration with start symbol."""
        return SCGConfiguration(String([self.start_symbol]))

    def direct_derive(self, configuration):
        """Perform direct derivation on configuration."""
        for rule in self.rules:
            try:
                yield from rule.apply(configuration)
            except Exception as e:
                print(f"Error while applying rule: {rule}")
                raise e


Rule = ScatteredContextRule
Grammar = ScatteredContextGrammar
