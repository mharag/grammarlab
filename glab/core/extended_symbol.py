from typing import Dict, Tuple

from glab.core.alphabet import NonTerminal as NonTerminalBase
from glab.core.alphabet import Symbol, SymbolType
from glab.core.alphabet import Terminal as TerminalBase


class ExtendedSymbol(Symbol):
    """ ExtendedSymbol is Symbol with additional flags

    For example if "S" is base symbol, extended symbol would be "S_current", "S_checked"...

    Attributes:
        variants: dictionary of all possible variants
            where key is variant name and value is tuple (Type, Representation),
            Type is either Terminal or NonTerminal
            Representation is unique str that will be displayed in sential form.

    Example:
        class ESymbol(ExtendedSymbol):
            variants = {
                "checked": (SymbolType.NON_TERMINAL, "C"),
            }

        symbol = ESymbol(Symbol("S"))
        symbol.id == "S"
        symbol.checked.id == "S_C"

    """
    _symbols = {}

    variants: Dict[str, Tuple[SymbolType, str]] = {}
    color = None

    def __new__(cls, base_symbol, symbol_id=None, symbol_type=None, variant=None):
        symbol_id = symbol_id or base_symbol.id
        symbol_type = symbol_type or base_symbol.type

        key = (cls, symbol_id, symbol_type, base_symbol, variant)
        if key not in cls._symbols:
            cls._symbols[key] = object.__new__(cls)

        return cls._symbols[key]

    def __init__(self, base_symbol, symbol_id=None, symbol_type=None, variant=None):
        self.base_symbol = base_symbol
        self.id = symbol_id or base_symbol.id
        self.type = symbol_type or base_symbol.type

        self.variant = variant

    def __getattr__(self, name: str):
        if name not in self.variants:
            raise AttributeError(f"Variant {name} not found")
        symbol_type, suffix = self.variants[name]
        symbol_id = self.base_symbol.id + "_" + suffix if suffix else None
        return self.__class__(
            symbol_id=symbol_id,
            symbol_type=symbol_type,
            base_symbol=self.base_symbol,
            variant=name,
        )

    @property
    def base(self):
        return self.__class__(self.base_symbol)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, type={self.type}, base_symbol={self.base_symbol})"


def get_symbol_factories(extended_symbol_class):
    def non_terminal(symbol_id):
        return extended_symbol_class(NonTerminal(symbol_id))

    def terminal(symbol_id):
        return extended_symbol_class(Terminal(symbol_id))

    return non_terminal, terminal


class Terminal(TerminalBase):
    variant = "terminal_base"
    base_symbol = None


class NonTerminal(NonTerminalBase):
    variant = "non_terminal_base"
    base_symbol = None
