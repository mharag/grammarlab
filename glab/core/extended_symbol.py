from typing import Dict, Tuple

from glab.core.alphabet import Symbol, Terminal as TerminalBase, NonTerminal as NonTerminalBase
from glab.core.alphabet import SymbolType
from glab.core.config import RESET, enabled


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
    symbols = {}

    base = (None, None)

    variants: Dict[str, Tuple[SymbolType, str]] = {}
    color = None

    def __new__(
        cls,
        base_symbol: Symbol,
        variant: str = None,
        symbol_type: SymbolType = None,
        variant_id: str = None
    ):
        key = (cls, base_symbol, variant, symbol_type, variant_id)
        if key not in cls.symbols:
            cls.symbols[key] = object.__new__(cls)
            cls.symbols[key].__init__(base_symbol, variant, symbol_type, variant_id)
        return cls.symbols[key]

    def __init__(
        self,
        base_symbol: Symbol,
        variant: str = None,
        symbol_type: SymbolType = None,
        variant_id: str = None
    ):
        self.base_symbol = base_symbol
        self.variant = variant
        self.type = symbol_type if symbol_type else base_symbol.type
        self.variant_id = variant_id

        if self.variant_id is None:
            self.id = self.base_symbol.id
        else:
            self.id = self.base_symbol.id + "_" + self.variant_id

    def __getattr__(self, name: str):
        if name not in self.variants:
            raise AttributeError(f"Variant {name} not found")
        return self.__class__(self.base_symbol, name, *self.variants[name])

    def __repr__(self):
        if self.variant_id is None:
            return str(self.base_symbol)
        if self.color and enabled:
            variant_id = f"{self.color}{self.variant_id}{RESET}"
        else:
            variant_id = self.variant_id
        return self.base_symbol.cli_output() + "_" + variant_id


class Terminal(TerminalBase):
    variant = "terminal_base"
    base_symbol = None


class NonTerminal(NonTerminalBase):
    variant = "non_terminal_base"
    base_symbol = None
