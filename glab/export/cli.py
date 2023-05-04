from glab.export.export import Export, formatter
from glab.grammars.phrase_grammar import PhraseGrammar, PhraseGrammarRule
from glab.grammars.scattered_context_grammar import ScatteredContextRule


class CliExport(Export):
    @formatter(PhraseGrammar)
    def grammar(self, grammar):
        rules = "\n".join([f"   {self.export(rule)}" for rule in grammar.rules])
        grammar_template = f"""{grammar.__class__.__name__}
Non-terminals: {str(grammar.non_terminals)}
Terminals: {str(grammar.terminals)}
Start symbol: {str(grammar.start_symbol)}
Rules:
{rules}"""
        return grammar_template

    @formatter(PhraseGrammarRule)
    def phrase_rule(self, rule):
        lhs = " ".join(map(str, rule.lhs))
        rhs = " ".join(map(str, rule.rhs))
        return f"{lhs} -> {rhs}"

    @formatter(ScatteredContextRule)
    def scattered_rule(self, rule):
        lhs = ",".join(map(str, rule.lhs))
        rhs = ",".join(map(str, rule.rhs))
        return f"({lhs}) -> ({rhs})"
