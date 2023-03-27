from generator.alphabet import N, T, A, S
from generator.grammar import Grammar


class ScatteredContextRule:
    def __init__(self, lhs: list[N], rhs: list[S]):
        if len(lhs) != len(rhs):
            raise ValueError(f"Different order of right and left side!")

        if not all([type(symbol) == N for symbol in lhs]):
            raise ValueError(f"Terminal symbol in left side of rule!")

        self.lhs = lhs
        self.rhs = rhs

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
            for cursor in range(self.order):
                derived.expand(match[cursor], self.rhs[cursor])
            yield derived


class ScatteredContextGrammar(Grammar):
    def __init__(self, non_terminals, terminals, rules: list[ScatteredContextRule], start_symbol):
        self.non_terminal = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol

    @property
    def axiom(self):
        return S([self.start_symbol])

    def direct_derive(self, string):
        for rule in self.rules:
            yield from rule.apply(string)


Rule = ScatteredContextRule
Grammar = ScatteredContextGrammar
