from typing import Dict, Tuple

from glab.alphabet import Symbol as SymbolBase
from glab.alphabet import SymbolType
from glab.config import RESET


class ExtendedSymbol(SymbolBase):
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
    base = (None, None)

    variants: Dict[str, Tuple[SymbolType, str]] = {}
    color = None

    def __init__(
        self,
        base_symbol: SymbolBase,
        variant: str = None,
        symbol_type: SymbolBase = None,
        variant_id: str = None
    ):
        self.base_symbol = base_symbol
        self.variant = variant
        self.type = symbol_type if symbol_type else base_symbol.type
        self.variant_id = variant_id

    @property
    def id(self):
        if self.variant_id is None:
            return self.base_symbol.id
        return self.base_symbol.id + "_" + self.variant_id

    def __getattr__(self, name: str):
        if name not in self.variants:
            raise AttributeError(f"Variant {name} not found")
        return self.__class__(self.base_symbol, name, *self.variants[name])

    def __repr__(self):
        if self.variant_id is None:
            return str(self.base_symbol)
        return f"{self.base_symbol}_{self.variant_id}"

    def cli_output(self):
        if self.variant_id is None:
            return str(self.base_symbol)
        if self.color:
            variant_id = f"{self.color}_{self.variant_id}{RESET}"
        else:
            variant_id = self.variant_id
        return self.base_symbol.cli_output() + variant_id


class Terminal(SymbolBase):
    type = SymbolType.TERMINAL
    variant = "terminal_base"
    base_symbol = None


class NonTerminal(SymbolBase):
    type = SymbolType.NON_TERMINAL
    variant = "non_terminal_base"
