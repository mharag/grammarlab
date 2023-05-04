from glab.export.export import Export, formatter
from glab.grammars.phrase_grammar import PhraseGrammar, PhraseGrammarRule
from glab.grammars.scattered_context_grammar import ScatteredContextRule


class LatexExport(Export):
    @formatter(PhraseGrammar)
    def grammar(self, grammar):
        lines = []
        for i in range(0, len(grammar.rules), 3):
            rules = grammar.rules[i:i + 3]
            parts = map(self.export, rules)
            line = "&" + ",\\quad &&".join(parts)
            lines.append(line)
        rules_str = "\\\\ \n \t\t".join(lines)

        grammar_template = rf"""\usepackage{{amsmath}}

\begin{{figure}}
    \begin{{eqnarray*}}
        N & = & \{{ {", ".join(map(str, grammar.non_terminals))} \}} \\
        T & = & \{{ {", ".join(map(str, grammar.terminals))} \}} \\\
        P & = & \left\{{ \begin{{aligned}}
                {rules_str}
                \end{{aligned}} \right\}} \\
        G & = & \{{N,T,P,{grammar.axiom}\}}
    \end{{eqnarray*}}
\end{{figure}}"""
        return grammar_template

    @formatter(PhraseGrammarRule)
    def phrase_rule(self, rule):
        lhs = r"\,".join(map(str, rule.lhs))
        rhs = r"\,".join(map(str, rule.rhs))
        return rf"{lhs} \Rightarrow {rhs}"

    @formatter(ScatteredContextRule)
    def scattered_rule(self, rule):
        lhs = r",\,".join(map(str, rule.lhs))
        rhs = r",\,".join(map(str, rule.rhs))
        return rf"({lhs}) \Rightarrow ({rhs})"
