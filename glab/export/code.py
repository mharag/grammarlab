from glab.core.alphabet import Alphabet
from glab.export.export import Export, formatter
from glab.grammars.phrase_grammar import PhraseGrammar, PhraseGrammarRule
from glab.grammars.scattered_context_grammar import (ScatteredContextGrammar,
                                                     ScatteredContextRule)


def list_to_str(l):
    return "[" + ", ".join([f'"{t}"' for t in l]) + "]"


def set_to_str(l):
    return "{" + ", ".join([f'"{t}"' for t in l]) + "}"


def string_to_str(string, delimiter=""):
    return '"'+(delimiter.join(map(str, string)))+'"'


class CodeExport(Export):
    @formatter(Alphabet)
    def alphabet(self, alphabet):
        return set_to_str(alphabet)

    @formatter(ScatteredContextGrammar)
    def scattered_context_grammar(self, grammar):
        return self.phrase_grammar(grammar, grammar_type="SCG")

    @formatter(PhraseGrammar)
    def phrase_grammar(self, grammar, grammar_type="RE"):
        rules = "\n".join([f"    {self.export(rule)}," for rule in grammar.rules])
        grammar_template = f"""\
from glab.core.cli import App
from glab.grammars.grammars import {grammar_type}

N = {self.export(grammar.non_terminals)}
T = {self.export(grammar.terminals)}
S = "{str(grammar.start_symbol)}"
P = [
{rules}
]

G = {grammar_type}(N, T, P, S)

if __name__ == "__main__":
    App(G).run()
"""
        return grammar_template

    @formatter(PhraseGrammarRule)
    def phrase_rule(self, rule):
        if any(len(symbol.id) > 1 for symbol in rule.lhs):
            lhs = list_to_str(rule.lhs)
        else:
            lhs = string_to_str(rule.lhs)
        if any(len(symbol.id) > 1 for symbol in rule.rhs):
            rhs = list_to_str(rule.rhs)
        else:
            rhs = string_to_str(rule.rhs)
        return f"({lhs}, {rhs})"

    @formatter(ScatteredContextRule)
    def scattered_rule(self, rule):
        lhs = list_to_str(rule.lhs)
        rhs = []
        for string in rule.rhs:
            if any(len(symbol.id) > 1 for symbol in string):
                rhs.append(list_to_str(string))
            else:
                rhs.append(string_to_str(string))
        rhs = "[" + (", ".join(rhs)) + "]"
        return f"({lhs}, {rhs})"
