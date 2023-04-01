from collections import defaultdict
import logging
from enum import Enum, auto
from glab.config import STRING_DELIMITER, COMPACT_REPR


log = logging.getLogger("glab.Alphabet")


class SymbolType(Enum):
    TERMINAL = "T"
    NON_TERMINAL = "N"


class Symbol:
    type = None

    def __init__(self, symbol):
        self._id = symbol

    def __eq__(self, other):
        return (
            isinstance(other, Symbol)
            and self.type == other.type
            and self.id == other.id
        )

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        # return  f"{self.__class__.__name__}({self.id}, type={self.type})"
        return self.id if COMPACT_REPR else f"{self.type.value}({self.id})"

    @property
    def id(self):
        return self._id

    def __add__(self, other):
        self_string = String([self])
        return self_string + other


class Terminal(Symbol):
    type = SymbolType.TERMINAL


class NonTerminal(Symbol):
    type = SymbolType.NON_TERMINAL



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



class String:
    def __init__(self, symbols: list[Symbol]):
        self.symbols = symbols

    @property
    def is_sentence(self):
        for symbol in self.symbols:
            if symbol.type != SymbolType.TERMINAL:
                return False
        return True

    def __str__(self):
        return STRING_DELIMITER.join([str(symbol) for symbol in self.symbols])

    def __repr__(self):
        if COMPACT_REPR:
            return str(self)
        return f"String({', '.join([repr(symbol) for symbol in self.symbols])})"

    def __eq__(self, other):
        return type(self) == type(other) and self.symbols == other.symbols

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
        log.debug(f"Creating index for string: {self}")
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
S = String
epsilon = T(None)
