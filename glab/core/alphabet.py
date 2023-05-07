import logging
from collections import defaultdict
from enum import Enum

from glab.core.representation import Representable

log = logging.getLogger("glab.Alphabet")


class SymbolType(Enum):
    TERMINAL = "T"
    NON_TERMINAL = "N"


class Symbol:
    _symbols = {}

    def __new__(cls, symbol_id, symbol_type):
        key = (cls, symbol_id, symbol_type)
        if key not in cls._symbols:
            cls._symbols[key] = super().__new__(cls)
        return cls._symbols[key]

    def __init__(self, symbol_id, symbol_type):
        self.id = symbol_id
        self.type = symbol_type

    def __eq__(self, other):
        #return self is other
        return self.id == other.id and self.type == other.type

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, type={self.type})"

    def __str__(self):
        return self.id

    def __add__(self, other):
        self_string = String([self])
        return self_string + other


class Terminal(Symbol):
    def __new__(cls, symbol_id):
        return Symbol(symbol_id, SymbolType.TERMINAL)


class NonTerminal(Symbol):
    def __new__(cls, symbol_id):
        return Symbol(symbol_id, SymbolType.NON_TERMINAL)



class Alphabet:
    def __init__(self, symbols: set[Symbol]):
        self.symbols = symbols
        self._symbol_lookup = {
            symbol.id: symbol for symbol in self.symbols
        }

    def __contains__(self, item):
        return item in self.symbols

    def __len__(self):
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)

    def union(self, other):
        return Alphabet(self.symbols | other.symbols)

    def __repr__(self):
        return f"Alphabet({{{str(self)}}})"

    def __str__(self):
        return ", ".join(str(symbol) for symbol in self.symbols)

    def lookup(self, symbol):
        if symbol not in self._symbol_lookup:
            raise ValueError(f"Symbol {symbol} ({type(symbol)}) not in alphabet!")
        return self._symbol_lookup[symbol]


class String(Representable):
    def __init__(self, symbols: list[Symbol]):
        self.symbols = symbols
        self.index = None
        self.create_index()

    @property
    def is_sentence(self):
        for symbol in self.symbols:
            if symbol.type != SymbolType.TERMINAL:
                return False
        return True

    def __repr__(self):
        symbols = ", ".join(repr(symbol) for symbol in self.symbols[:2])
        if len(self.symbols) > 2:
            symbols += ", ..."

        return f"{self.__class__.__name__}({symbols})"

    def __str__(self):
        return " ".join(map(str, self.symbols))

    def __eq__(self, other):
        return isinstance(other, String) and self.symbols == other.symbols

    def __len__(self):
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)

    def __getitem__(self, item):
        return self.symbols[item]

    def __add__(self, other):
        if isinstance(other, Symbol):
            other = String([other])
        elif not isinstance(other, String):
            raise TypeError(f"String cannot be concatenated with {type(other)}")
        return String(self.symbols + other.symbols)

    def create_index(self, symbols=None):
        index = defaultdict(list)
        for idx, symbol in enumerate(self.symbols):
            if symbols is None or symbol in symbols:
                index[symbol].append(idx)

        self.index = index

    def copy(self):
        return String(self.symbols.copy())

    def replace(self, index, symbol):
        self.symbols[index] = symbol
        self.create_index()

    def expand(self, index, string, expand_symbols=1):
        self.symbols[index:index+expand_symbols] = string.symbols
        self.create_index()


epsilon = Terminal(None)
