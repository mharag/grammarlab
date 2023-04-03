from glab.alphabet import Symbol as SymbolBase
from glab.alphabet import SymbolType
from glab.config import RESET


class ExtendedSymbol(SymbolBase):
    base = (None, None)
    variants = {}
    color = None

    def __init__(self, base_symbol, variant=None, symbol_type=None, variant_id=None):
        self.base_symbol = base_symbol
        self.variant = variant
        self.type = symbol_type if symbol_type else base_symbol.type
        self.variant_id = variant_id

    @property
    def id(self):
        if self.variant_id is None:
            return self.base_symbol.id
        return self.base_symbol.id + "_" + self.variant_id

    def __getattr__(self, name):
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
