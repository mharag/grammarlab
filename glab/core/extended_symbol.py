from typing import Dict, Tuple

from glab.core.alphabet import NonTerminal, Symbol, SymbolType, Terminal
from glab.core.config import Color


class ExtendedSymbol(Symbol):
    """ ExtendedSymbol is Symbol with additional flags

    For example if "S" is base symbol, extended symbol would be "S_current", "S_checked"...
    To use this class subclass it and define class variable variants.
    If you need complicated behavior you can define custom property instead of variable variant.

    Symbols are cached, so if you create symbol with same parameters it will return same object.

    Example:
        >>> class ESymbol(ExtendedSymbol):
        ...     variants = {
        ...         "checked": (SymbolType.NON_TERMINAL, "C"),
        ...     }
        ...
        >>> symbol = ESymbol(Symbol("S"))
        >>> symbol.id
        S
        >>> symbol.checked.id
        S_C
        >>> symbol.checked.base.id
        S

        Custom property variant:

        >>> class ESymbol(ExtendedSymbol):
        ...     @property
        ...     def upper(self):
        ...         return self.__class__(self.base_symbol, symbol_id=self.id.upper())
        ...
        >>> symbol = ESymbol(Symbol("s"))
        >>> symbol.upper.id
        S

    Properties and variant variable can be combined. Properties have higher priority.

    """
    _symbols = {}

    variants: Dict[str, Tuple[SymbolType, str]] = {}
    """ Dictionary of all possible variants.

    Key is variant name and value is tuple (Type, Representation),
    Type is either Terminal or NonTerminal
    Representation is unique str that will be displayed in sential form.

    """

    color: Color = None
    """ You can set color that will be used for exporting symbol to cli.

    All additional information added by this class will be highlighted with this color.
    If you want to used color you need to enable it in :mod:`glab.core.config`.
    Color can be set for each subclass separately. If None color is disabled.

    """

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
        symbol_id = (self.base_symbol.id + "_" + suffix) if suffix else None
        return self.__class__(
            symbol_id=symbol_id,
            symbol_type=symbol_type,
            base_symbol=self.base_symbol,
            variant=name,
        )

    @property
    def base(self) -> "ExtendedSymbol":
        """Return base symbol.

        Base is implicit variant that every ExtendedSymbol has.
        It returns symbol Extended symbol with same ID and type as base symbol.

        """
        return self.__class__(self.base_symbol)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, type={self.type}, base_symbol={self.base_symbol})"


def get_symbol_factories(extended_symbol_class: ExtendedSymbol) -> Tuple[callable, callable]:
    """Return functions for creating non-terminal and terminal extended symbols.

    Args:
        extended_symbol_class: ExtendedSymbol subclass that will be used for creating symbols.

    Returns:
        Tuple of functions for creating non terminal and terminal symbols.

    """
    def non_terminal(symbol_id: str) -> ExtendedSymbol:
        return extended_symbol_class(NonTerminal(symbol_id))

    def terminal(symbol_id: str) -> ExtendedSymbol:
        return extended_symbol_class(Terminal(symbol_id))

    return non_terminal, terminal
