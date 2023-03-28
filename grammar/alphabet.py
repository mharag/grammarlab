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


class CommunicationSymbol(Symbol):
    pass


class Alphabet:
    def __init__(self, symbols: set[Symbol]):
        self.symbols = symbols
        self._symbol_lookup = {
            symbol.symbol: symbol for symbol in self.symbols
        }

    def __contains__(self, item):
        return item in self.symbols

    def __len__(self):
        return len(self.symbols)

    def union(self, other):
        return Alphabet(self.symbols | other.symbols)

    def __repr__(self):
        return f"Alphabet({{{str(self)}}})"

    def __str__(self):
        return ", ".join(str(symbol) for symbol in self.symbols)

    def lookup(self, symbol):
        if symbol not in self._symbol_lookup:
            raise ValueError(f"Symbol {symbol} not in alphabet!")
        return self._symbol_lookup[symbol]



class String:
    def __init__(self, symbols: list[Symbol]):
        self.symbols = symbols

    @property
    def is_sentence(self):
        for symbol in self.symbols:
            if type(symbol) != Terminal:
                return False
        return True

    @property
    def is_communication(self):
        for symbol in self.symbols:
            if type(symbol) == CommunicationSymbol:
                return True
        return False

    def __repr__(self):
        return "".join([str(symbol) for symbol in self.symbols])

    def __eq__(self, other):
        return type(self) == type(other) and self.symbols == other.symbols

    def __len__(self):
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)

    def __getitem__(self, item):
        return self.symbols[item]

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

    def expand(self, index, string, expand_symbols=1):
        self.symbols[index:index+expand_symbols] = string.symbols


A = Alphabet
N = NonTerminal
T = Terminal
C = CommunicationSymbol
S = String
