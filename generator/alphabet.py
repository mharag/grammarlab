from collections import defaultdict


class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return type(self) == type(other) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __repr__(self):
        return self.symbol


class Terminal(Symbol):
    pass


class NonTerminal(Symbol):
    pass


class Alphabet:
    def __init__(self, symbols: set[Symbol]):
        self.symbols = symbols

    def __contains__(self, item):
        return item in self.symbols

    def __len__(self):
        return len(self.symbols)

    def union(self, other):
        return Alphabet(self.symbols | other.symbols)

    def __repr__(self):
        symbols = ", ".join(str(symbol) for symbol in self.symbols)
        return f"Alphabet({{{symbols}}})"


class String:
    def __init__(self, symbols: list[Symbol]):
        self.symbols = symbols

    @property
    def is_terminal(self):
        for symbol in self.symbols:
            if type(symbol) == NonTerminal:
                return False
        return True

    def __repr__(self):
        return "".join([str(symbol) for symbol in self.symbols])

    def __eq__(self, other):
        return self.symbols == other.symbols

    def create_index(self, symbols=None):
        index = defaultdict(list)
        for idx, symbol in enumerate(self.symbols):
            if symbols is None or symbol in symbols:
                index[symbol].append(idx)

        return index

    def copy(self):
        return String(self.symbols.copy())

    def replace(self, index, symbol):
        self.symbols[index] = symbol

    def expand(self, index, string):
        self.symbols[index:index+1] = string.symbols


A = Alphabet
N = NonTerminal
T = Terminal
S = String
