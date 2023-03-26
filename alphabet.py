class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return type(self) == type(other) and self.symbol == other.symbol


class Terminal(Symbol):
    pass


class NonTerminal(Symbol):
    pass


class Alphabet:
    def __init__(self, symbols: list[Symbol]):
        self.symbols = symbols

    def __contains__(self, item):
        return item in self.symbols