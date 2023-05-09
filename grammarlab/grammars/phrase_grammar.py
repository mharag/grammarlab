"""Phrase grammar.

"""
from typing import Generator, List

from grammarlab.core.common import Alphabet, String, Symbol, SymbolType
from grammarlab.core.grammar import Configuration, Grammar, Rule


class PhraseConfiguration(Configuration):
    """Configuration for phrase grammars is simple sential form."""
    #data: String
    #used_rule: "PhraseRule"
    #affected: List[int]

    @property
    def sential_form(self):
        return self.data


class PhraseRule(Rule):
    index = 0

    def __init__(self, lhs: String, rhs: String):
        super().__init__()
        if not all(symbol.type == SymbolType.NON_TERMINAL for symbol in lhs):
            raise ValueError(f"Terminal symbol in left side of rule! {lhs}")

        self.lhs = lhs
        self.rhs = rhs
        PhraseRule.index += 1
        self.label = f"p{self.index}"

    def __repr__(self):
        return f"{self.lhs} -> {self.rhs}"

    def match(self, sential_form: String) -> Generator[int, None, None]:
        """Find all matches of rule in sential form

        Args:
            sential_form: Sentence to match rule against.

        Returns:
            Generator of positions where rule matches.

        """
        index = sential_form.index
        for pos in index[self.lhs[0]]:
            if len(sential_form) < pos + len(self.lhs):
                continue
            for offset, symbol in enumerate(self.lhs):
                if sential_form[pos+offset] != symbol:
                    break
            else:
                yield pos

    def apply(self, configuration):
        """Apply rule to configuration.

        Args:
            configuration: Configuration to apply rule to.

        Returns:
            Generator of new configurations.

        """

        sential_form = configuration.sential_form
        matches = self.match(sential_form)
        for match in matches:
            new_sential_form = sential_form.copy()
            # replace lhs with rhs
            new_sential_form.expand(match, self.rhs, expand_symbols=len(self.lhs))
            new_configuration = PhraseConfiguration(new_sential_form, parent=configuration, used_rule=self, affected=match, depth=configuration.depth+1)
            yield new_configuration


class PhraseGrammar(Grammar):
    """Phrase grammar.

    """
    configuration_class = PhraseConfiguration

    def __init__(
        self,
        non_terminals: Alphabet,
        terminals: Alphabet,
        rules: List[PhraseRule],
        start_symbol: Symbol,
    ):
        super().__init__()
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol

    @property
    def axiom(self):
        """Configuration that starts derivation.
        """
        return PhraseConfiguration(String([self.start_symbol]))

    def direct_derive(self, configuration: PhraseConfiguration) -> Generator[PhraseConfiguration, None, None]:
        """One derivation step.

        Args:
            configuration: Configuration to derive.

        Returns:
            Generator of configurations that can be derived from given configuration.

        """
        # Apply all rules to configuration
        for rule in self.rules:
            yield from rule.apply(configuration)


class ContextFreeRule(PhraseRule):
    """Context free grammar.

    """

    def __init__(self, lhs: String, rhs: String):
        # check if rule is context free
        if len(lhs) > 1:
            raise ValueError("Context free grammar can only have single non-terminal in left side of rule!")
        super().__init__(lhs, rhs)

    def match(self, sential_form: String) -> Generator[int, None, None]:
        """All sentences can be generated by leftmost derivation.

        """
        for index, symbol in enumerate(sential_form):
            if symbol.type == SymbolType.NON_TERMINAL:
                break
        else:
            return

        left_most = next(super().match(sential_form), None)
        if left_most is not None and left_most == index:
            yield left_most



def length_preserving(grammar: PhraseGrammar):
    """Check if grammar is length preserving.

    Length preserving grammar is context grammar.

    Args: PhraseGrammar to check.
    Raises: ValueError if grammar is not length preserving.
    """
    for rule in grammar.rules:
        if len(rule.lhs) > len(rule.rhs):
            raise ValueError("Grammar contains shortening!")


def context_free(grammar: PhraseGrammar):
    """Check if grammar is context free."""
    for rule in grammar.rules:
        if len(rule.lhs) > 1:
            raise ValueError("Grammar contains context-sensitive rules!")
