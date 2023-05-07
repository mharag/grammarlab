from glab.export.export import Export, formatter
from glab.grammars.pc_grammar_system import PCGrammarSystem
from glab.grammars.phrase_grammar import PhraseGrammar, PhraseRule
from glab.grammars.scattered_context_grammar import ScatteredContextRule


class LatexExport(Export):
    # phrase grammars
    @formatter(PhraseGrammar)
    def phrase_grammar(self, grammar, grammar_name="G"):
        lines = []
        for i in range(0, len(grammar.rules), 3):
            rules = grammar.rules[i:i + 3]
            parts = map(self.export, rules)
            line = "&" + ",\\quad &&".join(parts)
            lines.append(line)
        rules_str = "\\\\ \n \t\t".join(lines)

        grammar_template = rf"""\begin{{figure}}
    \begin{{eqnarray*}}
        N & = & \{{ {", ".join(map(str, grammar.non_terminals))} \}} \\
        T & = & \{{ {", ".join(map(str, grammar.terminals))} \}} \\\
        P & = & \left\{{ \begin{{aligned}}
                {rules_str}
                \end{{aligned}} \right\}} \\
        {grammar_name} & = & \{{N,T,P,{grammar.axiom}\}}
    \end{{eqnarray*}}
\end{{figure}}"""
        return grammar_template

    @formatter(PhraseRule)
    def phrase_rule(self, rule):
        lhs = r"\,".join(map(str, rule.lhs))
        rhs = r"\,".join(map(str, rule.rhs))
        return rf"{lhs} \Rightarrow {rhs}"

    # scattered context grammars
    @formatter(ScatteredContextRule)
    def scattered_rule(self, rule):
        lhs = r",\,".join(map(str, rule.lhs))
        rhs = r",\,".join(map(str, rule.rhs))
        return rf"({lhs}) \Rightarrow ({rhs})"

    @formatter(PCGrammarSystem)
    def pc_grammar_system(self, grammar, grammar_name="G"):
        components  = []
        for i, component in enumerate(grammar.components):
            component = self.export(component, grammar_name=f"C{i}")
            components.append(component)
        component_names = ", ".join([f"C{i}" for i in range(len(grammar.components))])
        components = "\n\n".join(components)
        communication_symbols = r"\{{" + ", ".join(map(str, grammar.communication_symbols)) + r"\}}"
        return rf"""{components}

\begin{{figure}}
    \begin{{eqnarray*}}
        {grammar_name} & = & \{{{communication_symbols}, {component_names}\}}
    \end{{eqnarray*}}
\end{{figure}}"""
