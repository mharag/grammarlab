from typing import Iterable, List, Set

from glab.core.alphabet import (Alphabet, NonTerminal, String, Symbol,
                                SymbolType, Terminal)
from glab.core.grammar import Grammar
from glab.grammars.pc_grammar_system import PCGrammarSystem
from glab.grammars.phrase_grammar import (ContextFreeRule, PhraseGrammar,
                                          PhraseRule)
from glab.grammars.scattered_context_grammar import (ScatteredContextGrammar,
                                                     ScatteredContextRule)


class CodeLoad:
    """Collection of static methods for working with compact definitions.

    CodeLoad is not Importer! CodeLoad is working with python code which is well-structured.
    Using Importer wouldn't make sense for python code.

    """
    @staticmethod
    def symbol(raw_symbol: str, symbol_type: SymbolType) -> Symbol:
        """Get symbol from compact definition.

        Args:
            raw_symbol: id of symbol
            symbol_type: type of symbol

        Returns:
            Symbol

        """
        type_to_factory = {
            SymbolType.TERMINAL: Terminal,
            SymbolType.NON_TERMINAL: NonTerminal,
        }
        return type_to_factory[symbol_type](raw_symbol)

    @staticmethod
    def alphabet(raw_alphabet: Set[str], symbol_type: SymbolType) -> Alphabet:
        """Get alphabet from compact definition.

        Args:
            raw_alphabet: set of symbols
            symbol_type: type of symbols

        Returns:
            Alphabet

        """
        symbols = {CodeLoad.symbol(raw_symbol, symbol_type) for raw_symbol in raw_alphabet}
        return Alphabet(symbols)

    @staticmethod
    def string(raw_string: str, alphabet: Alphabet, delimiter="") -> String:
        """Get string from compact definition.

        Args:
            raw_string: str
            alphabet: Alphabet containing all symbols from raw_string
            delimiter: delimiter that separates symbols in raw_string

        Returns:
            String

        """
        result = []
        if delimiter:
            raw_string = raw_string.split(delimiter)
        for symbol in raw_string:
            result.append(alphabet.lookup(symbol))
        return String(result)

    @staticmethod
    def phrase_grammar(raw_non_terminals: Set, raw_terminals: Set, raw_rules: List, raw_start_symbol: str):
        """Get phrase grammar from compact definition

        Args:
            raw_non_terminals: Non-terminal symbols.
            raw_terminals: Terminal symbols.
            raw_rules: List of rules.
            raw_start_symbol: Start symbol.

        Returns:
            PhraseGrammar.

        Example:

            >>> non_terminals = {"A", "B", "C", "D"}
            >>> terminals = {"a", "b", "c", "d"}
            >>> rules = [("AB", "CD"), ("A", "BC")]
            >>> start_symbol = "A"
            >>> CodeLoad.phrase_grammar(non_terminals, terminals, rules, start_symbol)
            PhraseGrammar(...)

        """
        non_terminals = CodeLoad.alphabet(raw_non_terminals, SymbolType.NON_TERMINAL)
        terminals = CodeLoad.alphabet(raw_terminals, SymbolType.TERMINAL)
        alphabet = non_terminals.union(terminals)
        rules = [CodeLoad.phrase_rule(raw_rule[0], raw_rule[1], alphabet) for raw_rule in raw_rules]
        start_symbol = CodeLoad.symbol(raw_start_symbol, SymbolType.NON_TERMINAL)
        return PhraseGrammar(non_terminals, terminals, rules, start_symbol)

    @staticmethod
    def context_free_grammar(raw_non_terminals: Set, raw_terminals: Set, raw_rules: List, raw_start_symbol: str):
        """Get context free grammar from compact definition

        Args:
            raw_non_terminals: Non-terminal symbols
            raw_terminals: Terminal symbols
            raw_rules: List of rules
            raw_start_symbol: Start symbol

        Returns:
            PhraseGrammar with context free rules

        """
        non_terminals = CodeLoad.alphabet(raw_non_terminals, SymbolType.NON_TERMINAL)
        terminals = CodeLoad.alphabet(raw_terminals, SymbolType.TERMINAL)
        alphabet = non_terminals.union(terminals)
        rules = [CodeLoad.context_free_rule(raw_rule[0], raw_rule[1], alphabet) for raw_rule in raw_rules]
        start_symbol = CodeLoad.symbol(raw_start_symbol, SymbolType.NON_TERMINAL)
        return PhraseGrammar(non_terminals, terminals, rules, start_symbol)

    @staticmethod
    def phrase_rule(raw_lhs: Iterable, raw_rhs: Iterable, alphabet: Alphabet):
        """Get phrase rule from compact definition.

        Args:
            raw_lhs: Left side of rule.
            raw_rhs: Right side of rule.
            alphabet: Alphabet containing all symbols from raw_lhs and raw_rhs.

        Returns:
            PhraseRule.

        """
        lhs = CodeLoad.string(raw_lhs, alphabet)
        rhs = CodeLoad.string(raw_rhs, alphabet)
        return PhraseRule(lhs, rhs)

    @staticmethod
    def context_free_rule(raw_lhs: Iterable, raw_rhs: Iterable, alphabet: Alphabet):
        """Get context free rule from compact definition.

        Args:
            raw_lhs: Left side of rule.
            raw_rhs: Right side of rule.
            alphabet: Alphabet containing all symbols from raw_lhs and raw_rhs.

        Returns:
            ContextFreeRule.

        """
        lhs = CodeLoad.string(raw_lhs, alphabet)
        rhs = CodeLoad.string(raw_rhs, alphabet)
        return ContextFreeRule(lhs, rhs)

    @staticmethod
    def scattered_context_grammar(raw_non_terminals: Set, raw_terminals: Set, raw_rules: List, raw_start_symbol: str):
        """Get scattered context grammar from compact definition.

        Args:
            raw_non_terminals: Set of non-terminal symbols represented by str.
            raw_terminals: Set of non-terminal symbols represented by str.
            raw_rules: List of rules. Each rule is tuple containing left and right side.
            raw_start_symbol: Start symbol represented by str.

        Returns:
            Scattered context grammar.

        """
        non_terminals = CodeLoad.alphabet(raw_non_terminals, SymbolType.NON_TERMINAL)
        terminals = CodeLoad.alphabet(raw_terminals, SymbolType.TERMINAL)
        alphabet = non_terminals.union(terminals)
        rules = [CodeLoad.scattered_context_rule(rule[0], rule[1], alphabet) for rule in raw_rules]
        start_symbol = CodeLoad.symbol(raw_start_symbol, SymbolType.NON_TERMINAL)
        return ScatteredContextGrammar(non_terminals, terminals, rules, start_symbol)

    @staticmethod
    def scattered_context_rule(raw_lhs: Iterable, raw_rhs: Iterable, alphabet: Alphabet):
        """Get scattered context rule from compact definition.

        Args:
            raw_lhs: Left side of rule.
            raw_rhs: Right side of rule.
            alphabet: Alphabet containing all symbols from raw_lhs and raw_rhs.

        Returns:
            ScatteredContextRule.

        """
        lhs = [alphabet.lookup(symbol) for symbol in raw_lhs]
        rhs = [CodeLoad.string(raw_string, alphabet) for raw_string in raw_rhs]
        return ScatteredContextRule(lhs, rhs)

    @staticmethod
    def pc_grammar_system(
        raw_communication_symbols: List[str],
        *components: List[Grammar],
        returning: bool = True,
    ):
        """Get PC grammar system from compact definition.

        Args:
            raw_communication_symbols: List of communication symbols.
            components: List of components.
            returning: If True, component is returned to its initial state after communication.

        Returns:
            PCGrammarSystem.

        """
        communication_symbols = [
            CodeLoad.symbol(raw_symbol, SymbolType.NON_TERMINAL) for raw_symbol in raw_communication_symbols
        ]
        return PCGrammarSystem(
            comumunication_symbols=communication_symbols,
            components=components,
            returning=returning,
        )
