from grammar.alphabet import N, T, A, S
from grammar.grammar import Grammar
from grammar.constructors import construct_nonterminal_alphabet, construct_terminal_alphabet, construct_rules, construct_string


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
        lhs = construct_string(alphabet, lhs)
        rhs = construct_string(alphabet, rhs)
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


class PhraseGrammar(Grammar):
    def __init__(self, non_terminals, terminals, rules: list[PhraseGrammarRule], start_symbol):
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
        non_terminals = construct_nonterminal_alphabet(non_terminals)
        terminals = construct_terminal_alphabet(terminals)
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
