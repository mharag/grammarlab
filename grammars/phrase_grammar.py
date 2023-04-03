from glab.alphabet import N, S
from glab.ast import Tree
from glab.compact_definition import (compact_nonterminal_alphabet,
                                     compact_string, compact_terminal_alphabet)
from glab.grammar_base import ConfigurationBase, GrammarBase
from grammars.pc_grammar_system import CommunicationRule


class PhraseConfiguration(ConfigurationBase):
    @property
    def sential_form(self):
        return self.data

    @property
    def is_sentence(self):
        return self.data.is_sentence

    def __repr__(self):
        return str(self.data)

    def create_ast(self, depth=0):
        if not self.parent:
            tree = Tree()
            root_node = tree.create_node(self.data[0], depth=depth)
            tree.add_root(root_node)
            return tree

        parent_ast = self.parent.create_ast(depth=depth+1)

        if self.used_production is None:
            new_node = parent_ast.create_node(self.data[0], depth)
            parent_ast.frontier[0].add_children([new_node])
            for parent in parent_ast.frontier[1:]:
                new_node.add_parent(parent)
                parent.remove_from_frontier()
            return parent_ast

        if isinstance(self.used_production, CommunicationRule):
            parents = [parent_ast.frontier[x] for x in self.affected]
            for parent in parents:
                symbol = parent.data
                rhs = self.used_production[symbol]
                children = [parent_ast.create_node(x, depth) for x in rhs]
                parent.add_children(children)
            return parent_ast

        self.apply_rule_to_ast(parent_ast, depth)
        return parent_ast

    def apply_rule_to_ast(self, parent_ast, depth):
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


class PhraseGrammarRule:
    index = 0

    def __init__(self, lhs: S, rhs: S):
        super().__init__()
        if not all(isinstance(symbol, N) for symbol in lhs):
            raise ValueError("Terminal symbol in left side of rule!")

        self.lhs = lhs
        self.rhs = rhs
        PhraseGrammarRule.index += 1
        self.label = f"p{self.index}"

    @classmethod
    def deserialize(cls, alphabet, rule):
        lhs, rhs = rule
        lhs = compact_string(alphabet, lhs)
        rhs = compact_string(alphabet, rhs)
        return cls(lhs, rhs)

    def __repr__(self):
        return f"{self.label}: {self.lhs} -> {self.rhs}"

    def match(self, string: S):
        index = string.create_index()
        for pos in index[self.lhs[0]]:
            if len(string) < pos + len(self.lhs):
                continue
            for offset, symbol in enumerate(self.lhs):
                if string[pos+offset] != symbol:
                    break
            else:
                yield pos

    def apply(self, configuration):
        sential_form = configuration.sential_form
        matches = self.match(sential_form)
        for match in matches:
            derived = sential_form.copy()
            offset = 0
            derived.expand(match+offset, self.rhs, expand_symbols=len(self.lhs))
            offset += len(self.rhs) - len(self.lhs)
            new_configuration = PhraseConfiguration(derived, parent=configuration, used_production=self, affected=match)
            yield new_configuration


class PhraseGrammar(GrammarBase):
    def __init__(self, non_terminals, terminals, rules: list[PhraseGrammarRule], start_symbol):
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

    def parse_configuration(self, representation, delimiter):
        return PhraseConfiguration(compact_string(self.terminals.union(self.non_terminals), representation, delimiter=delimiter))

    @classmethod
    def deserialize(cls, non_terminals, terminals, rules, start_symbol):
        non_terminals = compact_nonterminal_alphabet(non_terminals)
        terminals = compact_terminal_alphabet(terminals)
        alphabet = non_terminals.union(terminals)
        rules = [PhraseGrammarRule.deserialize(alphabet, rule) for rule in rules]
        start_symbol = N(start_symbol)
        return cls(non_terminals, terminals, rules, start_symbol)

    @property
    def axiom(self):
        return PhraseConfiguration(S([self.start_symbol]))

    def direct_derive(self, string):
        for rule in self.rules:
            yield from rule.apply(string)


def length_preserving(grammar):
    for rule in grammar.rules:
        if len(rule.lhs) > len(rule.rhs):
            raise ValueError("Grammar contains shortening!")


def context_free(grammar):
    for rule in grammar.rules:
        if len(rule.lhs) > 1:
            raise ValueError("Grammar contains context-sensitive rules!")
