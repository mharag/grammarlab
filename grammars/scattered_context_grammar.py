from glab.alphabet import N, T, A, S, Symbol
from glab.grammar_base import GrammarBase
from glab.compact_definition import compact_nonterminal_alphabet, compact_terminal_alphabet, compact_string


class ScatteredContextRule:
    def __init__(self, lhs: list[N], rhs: list[S]):
        super().__init__()
        if len(lhs) != len(rhs):
            raise ValueError(f"Different order of right and left side!")

        if not all([type(symbol) == N for symbol in lhs]):
            raise ValueError(f"Terminal symbol in left side of rule!")

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

    def apply(self, string: S):
        matches = self.match(string)
        for match in matches:
            derived = string.copy()
            offset = 0
            for cursor in range(self.order):
                derived.expand(match[cursor]+offset, self.rhs[cursor])
                offset += len(self.rhs[cursor]) - 1
            yield derived


class ScatteredContextGrammar(GrammarBase):
    def __init__(self, non_terminals, terminals, rules: list[ScatteredContextRule], start_symbol):
        super().__init__()
        self.non_terminal = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol

    def __str__(self):
        rules = "\n".join([f"- {rule}" for rule in self.rules])
        return f"""Scattered contex grammar
Non-terminals: {str(self.non_terminal)}
Terminals: {str(self.terminals)}
Rules: 
{rules}
        """

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
        return S([self.start_symbol])

    def direct_derive(self, string):
        for rule in self.rules:
            try:
                yield from rule.apply(string)
            except Exception as e:
                print(f"Error while applying rule: {rule}")
                raise e


Rule = ScatteredContextRule
Grammar = ScatteredContextGrammar
