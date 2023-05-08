"""Definitions of basic objects common to all grammars.

"""

import logging
from collections import defaultdict
from enum import Enum

log = logging.getLogger("glab.Alphabet")


class SymbolType(Enum):
    TERMINAL = "T"
    """Terminal symbol. Terminal can't be further expanded."""
    NON_TERMINAL = "N"
    """Non-terminal symbol. Non-terminal can be further expanded."""


class Symbol:
    """Class representing a symbol of a grammar.

    Symbols are either terminals or non-terminals. Symbols are identified by their id and type.
    Symbols are cached, so that only one instance of a symbol with a given id and type exists.

    Examples:
        Only one instance of a symbol with a given id and type exists.

        >>> Symbol("a", SymbolType.TERMINAL) is Symbol("a", SymbolType.TERMINAL)
        True

        Symbols can be added to create strings.

        >>> Symbol("a", SymbolType.TERMINAL) + Symbol("a", SymbolType.NON_TERMINAL)
        String(Symbol(id=a, type=SymbolType.TERMINAL), Symbol(id=a, type=SymbolType.NON_TERMINAL))

    """
    _symbols = {}

    def __new__(cls, symbol_id, symbol_type):
        key = (cls, symbol_id, symbol_type)
        # check if symbol already exists
        if key not in cls._symbols:
            # create new symbol
            cls._symbols[key] = super().__new__(cls)
        return cls._symbols[key]

    def __init__(self, symbol_id, symbol_type):
        self.id = symbol_id
        self.type = symbol_type

    def __eq__(self, other):
        return (
            isinstance(other, Symbol)
            and self.id == other.id
            and self.type == other.type
        )

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
    """Shortcut for creating a terminal symbol.

    Example:
        >>> Terminal("a") is Symbol("a", SymbolType.TERMINAL)
        True

    """
    def __new__(cls, symbol_id):
        return Symbol(symbol_id, SymbolType.TERMINAL)


class NonTerminal(Symbol):
    """Shortcut for creating a non-terminal symbol.

    Example:
        >>> NonTerminal("S") is Symbol("S", SymbolType.NON_TERMINAL)
        True

    """
    def __new__(cls, symbol_id):
        return Symbol(symbol_id, SymbolType.NON_TERMINAL)


epsilon = Terminal(None)


class Alphabet:
    """Class representing an alphabet.

    Alphabets are sets of symbols.
    Every alphabet contains the epsilon symbol. But it's not counted in the length of the alphabet
    and is not yielded when iterating over the alphabet.

    Examples:
        >>> alphabet = Alphabet({Terminal("a"), Terminal("b")})
        >>> [symbol for symbol in alphabet]
        [Symbol(id=a, type=SymbolType.TERMINAL), Symbol(id=b, type=SymbolType.TERMINAL)]
        >>> len(alphabet)
        2
        >>> Terminal("a") in alphabet
        True

    """
    def __init__(self, symbols: set[Symbol]):
        self.symbols = symbols | {epsilon}
        self._symbol_lookup = {
            symbol.id: symbol for symbol in self.symbols
        }

    def __contains__(self, item):
        return item in self.symbols

    def __len__(self):
        # Epsilon is always in the alphabet but should not be counted
        return len(self.symbols) - 1

    def __iter__(self):
        # do not yield implicit epsilon
        return iter(self.symbols - {epsilon})

    def union(self, other: "Alphabet") -> "Alphabet":
        """Return the union of two alphabets.

        Original alphabets are not modified.

        Args:
            other: The other alphabet.

        Returns:
            The union of the two alphabets.

        """
        return Alphabet(self.symbols | other.symbols)

    def __repr__(self):
        return f"Alphabet({self.symbols})"

    def lookup(self, raw_symbol: str) -> Symbol:
        """Search for a symbol in the alphabet by its id.

        Args:
            raw_symbol: The id of the symbol to look up.

        Returns:
            The symbol with the given id.

        Example:
            >>> alphabet = Alphabet({Terminal("a"), Terminal("b")})
            >>> alphabet.lookup("a")
            Symbol(id=a, type=SymbolType.TERMINAL)

        """
        if raw_symbol not in self._symbol_lookup:
            raise ValueError(f"Symbol {raw_symbol} ({type(raw_symbol)}) not in alphabet!")
        return self._symbol_lookup[raw_symbol]


class String:
    """Class representing a sequences of symbols.

    Epsilon is automatically removed from the string.

    Examples:
        >>> string1 = String([Terminal("a")])
        >>> string2 = String([NonTerminal("b")])
        >>> string1 + string2
        String(Symbol(id=a, type=SymbolType.TERMINAL), Symbol(id=b, type=SymbolType.NON_TERMINAL))
        >>> len(string1)
        1
        >>> string1[0]
        Symbol(id=a, type=SymbolType.TERMINAL)

    """

    def __init__(self, symbols: list[Symbol]):
        # Remove epsilon from string
        self.symbols = list(filter(lambda symbol: symbol != epsilon, symbols))
        self.index = None
        """Index of the string.
        
        The index is a dictionary mapping symbols to their positions in the string.
        
        """
        self._create_index()

    @property
    def is_sentence(self):
        """Check if the string is a sentence.

        A string is a sentence if it only contains terminal symbols.

        """
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

    def _create_index(self):
        index = defaultdict(list)
        for idx, symbol in enumerate(self.symbols):
            index[symbol].append(idx)

        self.index = index

    def copy(self) -> "String":
        """Return a copy of the string."""
        return String(self.symbols.copy())

    def replace(self, index: int, symbol: Symbol):
        """Replace a symbol in the string with another symbol."""
        self.symbols[index] = symbol
        self._create_index()

    def expand(self, index: int, string: "String", expand_symbols: int = 1):
        """Replace a symbols in the string with a string of symbols.

        Args:
            index: The index of the first symbol to replace.
            string: The string to insert.
            expand_symbols: The number of symbols to replace.

        """
        self.symbols[index:index+expand_symbols] = string.symbols
        self._create_index()
