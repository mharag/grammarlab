from typing import Generator, Iterable, List, Set, Tuple

from glab.core.alphabet import (Alphabet, NonTerminal, String, Symbol,
                                SymbolType)
from glab.core.ast import Tree
from glab.core.compact_definition import (compact_nonterminal_alphabet,
                                          compact_string,
                                          compact_terminal_alphabet)
from glab.core.grammar_base import (ConfigurationBase, GrammarBase,
                                    ProductionBase)
from glab.grammars.pc_grammar_system import CommunicationRule


class PhraseConfiguration(ConfigurationBase):
    """Configuration for phrase grammars is simple sential form."""

    @property
    def sential_form(self):
        return self.data

    @classmethod
    def deserialize(cls, grammar: "PhraseGrammar", representation: str, delimiter: str):
        """Deserialize configuration from string.

        Example of string representation:
            ABCD
            aaaAAAA
            S_G,B_G,C_G,D_G (delimeter is ',')

        Args:
            grammar: Grammar that this configuration belongs to.
            representation: String representation of configuration.
            delimiter: Delimiter used to separate symbols of sential form.

        Returns:
            PhraseConfiguration instance.

        """

        sential_form = compact_string(
            grammar.non_terminals.union(grammar.terminals),
            representation,
            delimiter=delimiter
        )
        return cls(sential_form)

    def __repr__(self):
        return self.data

    def create_ast_root(self, depth) -> Tree:
        # create root node
        tree = Tree()
        root_node = tree.create_node(self.data[0], depth=depth)
        tree.add_root(root_node)
        return tree

    def create_ast_pc_grammar(self, depth: int = 0) -> Tree:
        if not self.parent:
            parent_ast = self.create_ast_root(depth)
            return parent_ast
        # recursively create AST from parent
        parent_ast = self.parent.create_ast_pc_grammar(depth=depth+1)

        if self.used_production is None:
            # return grammar to start symbol - used by PC grammar systems
            new_node = parent_ast.create_node(self.data[0], depth)
            parent_ast.frontier[0].add_children([new_node])
            for parent in parent_ast.frontier[1:]:
                new_node.add_parent(parent)
                parent.remove_from_frontier()
            return parent_ast

        if isinstance(self.used_production, CommunicationRule):
            # replace communication symbols
            parents = [parent_ast.frontier[x] for x in self.affected]
            for parent in parents:
                symbol = parent.data
                rhs = self.used_production[symbol]
                children = [parent_ast.create_node(x, depth) for x in rhs]
                parent.add_children(children)
            return parent_ast

        # apply rule to parent AST
        self.apply_rule_to_ast(parent_ast, depth)
        return parent_ast

    def create_ast(self, depth: int = 0) -> Tree:
        """Create AST from configuration.
        """

        if not self.parent:
            parent_ast = self.create_ast_root(depth)
            return parent_ast
        # recursively create AST from parent
        parent_ast = self.parent.create_ast(depth=depth+1)

        # apply rule to parent AST
        self.apply_rule_to_ast(parent_ast, depth)
        return parent_ast

    def apply_rule_to_ast(self, parent_ast: Tree, depth: int) -> Tree:
        """ Incrementally apply rule to parent AST."""
        # multiple parents can be affected by context rule
        parents = parent_ast.frontier[self.affected:self.affected + len(self.used_production.lhs)]
        children = [parent_ast.create_node(x, depth) for x in self.used_production.rhs]
        parents[0].add_children(children)
        for parent in parents[1:]:
            parent.remove_from_frontier()
            for child in children:
                child.add_parent(parent)
        return parent_ast

    def __str__(self):
        return str(self.data)


class PhraseGrammarRule(ProductionBase):
    index = 0

    def __init__(self, lhs: String, rhs: String):
        super().__init__()
        if not all(symbol.type == SymbolType.NON_TERMINAL for symbol in lhs):
            raise ValueError(f"Terminal symbol in left side of rule! {lhs}")

        self.lhs = lhs
        self.rhs = rhs
        PhraseGrammarRule.index += 1
        self.label = f"p{self.index}"

    @classmethod
    def deserialize(cls, alphabet: Alphabet, representation: Tuple[Iterable, Iterable]):
        """Deserialize rule.

        Serialized rule is tuple containing left and right side.
        Each side is represented as list or string of symbols.
        Examples of serialized rules:
            (["A", "B"], ["C", "D"]), (["A", "B"], "CD")

        """
        lhs, rhs = representation
        lhs = compact_string(alphabet, lhs)
        rhs = compact_string(alphabet, rhs)
        return cls(lhs, rhs)

    def __repr__(self):
        return f"{self.lhs} -> {self.rhs}"

    def match(self, sential_form: String) -> Generator[int, None, None]:
        """Find all matches of rule in sential form

        Args:
            sential_form: Sentence to match rule against.

        Returns:
            Generator of positions where rule matches.

        """
        index = sential_form.create_index()
        for pos in index[self.lhs[0]]:
            if len(sential_form) < pos + len(self.lhs):
                continue
            for offset, symbol in enumerate(self.lhs):
                if sential_form[pos+offset] != symbol:
                    break
            else:
                yield pos

    def apply(self, configuration):
        """Apply rule to configuration.

        Args:
            configuration: Configuration to apply rule to.

        Returns:
            Generator of new configurations.

        """

        sential_form = configuration.sential_form
        matches = self.match(sential_form)
        for match in matches:
            new_sential_form = sential_form.copy()
            # replace lhs with rhs
            new_sential_form.expand(match, self.rhs, expand_symbols=len(self.lhs))
            new_configuration = PhraseConfiguration(new_sential_form, parent=configuration, used_production=self, affected=match, depth=configuration.depth+1)
            yield new_configuration


class PhraseGrammar(GrammarBase):
    """Phrase grammar.

    """
    configuration_class = PhraseConfiguration

    def __init__(
        self,
        non_terminals: Alphabet,
        terminals: Alphabet,
        rules: List[PhraseGrammarRule],
        start_symbol: Symbol,
    ):
        super().__init__()
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol

    def __str__(self):
        rules = "\n".join([f"- {rule}" for rule in self.rules])
        return f"""{self.__class__.__name__}
Non-terminals: {str(self.non_terminals)}
Terminals: {str(self.terminals)}
Start symbol: {self.start_symbol}
Rules:
{rules}
        """

    def deserialize_configuration(self, representation, delimiter):
        """Deserialize configuration.

        Args:
            representation: Representation of configuration.
            delimiter: delimiter used to separate symbols in representation.

        Returns:
            Configuration.

        """
        return PhraseConfiguration(
            compact_string(self.terminals.union(self.non_terminals), representation, delimiter=delimiter)
        )

    @classmethod
    def deserialize(
        cls,
        non_terminals: Set,
        terminals: Set,
        rules: List[Tuple[Iterable, Iterable]],
        start_symbol: str
    ):
        """Deserialize grammar.

        Examples of serialized grammar:
            non_terminals = {"A", "B", "C", "D"}
            terminals = {"a", "b", "c", "d"}
            rules = [("AB", "CD"), ("A", "BC")]
            start_symbol = "A"

        Args:
            non_terminals: Non-terminal symbols.
            terminals: Terminal symbols.
            rules: List of rules.
            start_symbol: Start symbol.
        Returns:
            PhraseGrammar.

        """
        non_terminals = compact_nonterminal_alphabet(non_terminals)
        terminals = compact_terminal_alphabet(terminals)
        alphabet = non_terminals.union(terminals)
        rules = [PhraseGrammarRule.deserialize(alphabet, rule) for rule in rules]
        start_symbol = NonTerminal(start_symbol)
        return cls(non_terminals, terminals, rules, start_symbol)

    @property
    def axiom(self):
        """Configuration that starts derivation.
        """
        return PhraseConfiguration(String([self.start_symbol]))

    def direct_derive(self, configuration: PhraseConfiguration) -> Generator[PhraseConfiguration, None, None]:
        """One derivation step.

        Args:
            configuration: Configuration to derive.

        Returns:
            Generator of configurations that can be derived from given configuration.

        """
        # Apply all rules to configuration
        for rule in self.rules:
            yield from rule.apply(configuration)


def length_preserving(grammar: PhraseGrammar):
    """Check if grammar is length preserving.

    Length preserving grammar is context grammar.

    Args: PhraseGrammar to check.
    Raises: ValueError if grammar is not length preserving.
    """
    for rule in grammar.rules:
        if len(rule.lhs) > len(rule.rhs):
            raise ValueError("Grammar contains shortening!")


def context_free(grammar: PhraseGrammar):
    """Check if grammar is context free."""
    for rule in grammar.rules:
        if len(rule.lhs) > 1:
            raise ValueError("Grammar contains context-sensitive rules!")
