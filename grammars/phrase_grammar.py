from glab.alphabet import N, T, A, S
from glab.grammar_base import GrammarBase
from glab.compact_definition import compact_nonterminal_alphabet, compact_terminal_alphabet, compact_rules, compact_string


class PhraseGrammarRule:
    def __init__(self, lhs: S, rhs: S):
        super().__init__()
        if not all([type(symbol) == N for symbol in lhs]):
            raise ValueError(f"Terminal symbol in left side of rule!")

        self.lhs = lhs
        self.rhs = rhs

    @classmethod
    def construct(cls, alphabet, rule):
        lhs, rhs = rule
        lhs = compact_string(alphabet, lhs)
        rhs = compact_string(alphabet, rhs)
        return cls(lhs, rhs)

    def __repr__(self):
        return f"{self.lhs} -> {self.rhs}"

    def match(self, string: S):
        index = string.create_index()
        for pos in index[self.lhs[0]]:
            if len(string) < pos + len(self.lhs):
                continue
            for offset, symbol in enumerate(self.lhs):
                if string[pos+offset] != symbol:
                    break
            else:
                yield pos

    def apply(self, string: S):
        matches = self.match(string)
        for match in matches:
            derived = string.copy()
            offset = 0
            derived.expand(match+offset, self.rhs, expand_symbols=len(self.lhs))
            offset += len(self.rhs) - len(self.lhs)
            yield derived


class PhraseGrammar(GrammarBase):
    def __init__(self, non_terminals, terminals, rules: list[PhraseGrammarRule], start_symbol):
        super().__init__()
        self.non_terminal = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol

    def __str__(self):
        rules = "\n".join([f"- {rule}" for rule in self.rules])
        return f"""Phrase grammar
Non-terminals: {str(self.non_terminal)}
Terminals: {str(self.terminals)}
Rules: 
{rules}
        """

    @classmethod
    def construct(cls, non_terminals, terminals, rules, start_symbol):
        non_terminals = compact_nonterminal_alphabet(non_terminals)
        terminals = compact_terminal_alphabet(terminals)
        alphabet = non_terminals.union(terminals)
        rules = [PhraseGrammarRule.construct(alphabet, rule) for rule in rules]
        start_symbol = N(start_symbol)
        return cls(non_terminals, terminals, rules, start_symbol)

    @property
    def axiom(self):
        return S([self.start_symbol])

    def direct_derive(self, string):
        for rule in self.rules:
            yield from rule.apply(string)


def length_preserving(grammar):
    for rule in grammar.rules:
        if len(rule.lhs) < len(rule.rhs):
            return ValueError("Grammar contains shortening!")


def context_free(grammar):
    for rule in grammar.rules:
        if len(rule.lhs) > 1:
            return ValueError("Grammar contains context-sensitive rules!")