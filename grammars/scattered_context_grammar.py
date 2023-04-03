from glab.alphabet import N, S, Symbol, SymbolType
from glab.compact_definition import (compact_nonterminal_alphabet,
                                     compact_string, compact_terminal_alphabet)
from grammars.phrase_grammar import PhraseConfiguration, PhraseGrammar


class SCGConfiguration(PhraseConfiguration):
    @property
    def sential_form(self):
        return self.data

    @property
    def is_sentence(self):
        return self.data.is_sentence

    def apply_rule_to_ast(self, parent_ast, depth=0):
        lhs_nodes = []
        for position in self.affected:
            lhs_nodes.append(parent_ast.frontier[position])

        for i, string in enumerate(self.used_rule.rhs):
            children = [parent_ast.create_node(x, depth) for x in string]
            lhs_nodes[i].add_children(children)
        return parent_ast

    def __str__(self):
        return str(self.data)


class ScatteredContextRule:
    def __init__(self, lhs: list[N], rhs: list[S]):
        super().__init__()
        if len(lhs) != len(rhs):
            raise ValueError("Different order of right and left side!")

        if not all(symbol.type == SymbolType.NON_TERMINAL for symbol in lhs):
            raise ValueError("Terminal symbol in left side of rule!")

        self.lhs = lhs

        unified_rhs = []
        for item in rhs:
            if isinstance(item, Symbol):
                item = S([item])
            unified_rhs.append(item)
        self.rhs = unified_rhs

    @classmethod
    def construct(cls, alphabet, rule):
        lhs, rhs = rule
        lhs = [alphabet.lookup(symbol) for symbol in lhs]
        rhs = [compact_string(alphabet, string) for string in rhs]
        return cls(lhs, rhs)

    def __repr__(self):
        lhs = ", ".join(str(symbol) for symbol in self.lhs)
        rhs = ", ".join(str(string) for string in self.rhs)
        return f"({lhs}) -> ({rhs})"

    @property
    def order(self):
        return len(self.lhs)

    @staticmethod
    def find_next(index, string_position, last, symbol):
        start = 0 if last == -1 else last + 1
        for i in range(start, len(index[symbol])):
            if index[symbol][i] > string_position:
                return i
        return -1

    def match(self, string: S):
        index = string.create_index(self.lhs)
        index_positions = [-1] * self.order

        cursor = 0
        while cursor >= 0:
            if cursor >= self.order:
                yield [index[self.lhs[i]][index_positions[i]] for i in range(self.order)]
                cursor -= 1

            string_position = -1 if cursor == 0 else index[self.lhs[cursor-1]][index_positions[cursor-1]]

            symbol = self.lhs[cursor]
            next_position = self.find_next(index, string_position, index_positions[cursor], symbol)
            if next_position == -1:
                index_positions[cursor] = -1
                cursor -= 1
            else:
                index_positions[cursor] = next_position
                cursor += 1

    def apply(self, configration: SCGConfiguration):
        sential_form = configration.sential_form
        matches = self.match(sential_form)
        for match in matches:
            derived = sential_form.copy()
            offset = 0
            for cursor in range(self.order):
                derived.expand(match[cursor]+offset, self.rhs[cursor])
                offset += len(self.rhs[cursor]) - 1
            new_configuration = SCGConfiguration(derived, parent=configration, used_rule=self, affected=match)
            yield new_configuration


class ScatteredContextGrammar(PhraseGrammar):
    configuration = SCGConfiguration

    def parse_configuration(self, representation, delimiter):
        return SCGConfiguration(compact_string(self.terminals.union(self.non_terminals), representation, delimiter=delimiter))

    @classmethod
    def construct(cls, non_terminals, terminals, rules, start_symbol):
        non_terminals = compact_nonterminal_alphabet(non_terminals)
        terminals = compact_terminal_alphabet(terminals)
        alphabet = non_terminals.union(terminals)
        rules = [ScatteredContextRule.construct(alphabet, rule) for rule in rules]
        start_symbol = N(start_symbol)
        return cls(non_terminals, terminals, rules, start_symbol)

    @property
    def axiom(self):
        return SCGConfiguration(S([self.start_symbol]))

    def direct_derive(self, configuration):
        for rule in self.rules:
            try:
                yield from rule.apply(configuration)
            except Exception as e:
                print(f"Error while applying rule: {rule}")
                raise e


Rule = ScatteredContextRule
Grammar = ScatteredContextGrammar
