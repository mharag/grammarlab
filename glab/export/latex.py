from glab.export.export import Export, formatter
from glab.grammars.pc_grammar_system import PCGrammarSystem
from glab.grammars.phrase_grammar import PhraseGrammar, PhraseRule, PhraseConfiguration
from glab.grammars.scattered_context_grammar import ScatteredContextRule
from glab.core.alphabet import Alphabet, Symbol, String


class LatexExport(Export):
    @formatter(Alphabet)
    def Alphabet(self, alphabet):
        return r"\{" + r",\,".join(map(self.export, alphabet)) + r"\}"

    @formatter(Symbol)
    def Symbol(self, symbol):
        return symbol.id

    @formatter(String)
    def String(self, string):
        return r"\,".join(map(self.export, string))

    @formatter(PhraseConfiguration)
    def PhraseConfiguration(self, config):
        return self.export(config.sential_form)

    # phrase grammars
    @formatter(PhraseGrammar)
    def PhraseGrammar(self, grammar, grammar_name="G"):
        """Also can export subclass :class:`glab.grammars.scattered_context_grammar.ScatteredContextGrammar`

        """
        lines = []
        for i in range(0, len(grammar.rules), 3):
            rules = grammar.rules[i:i + 3]
            parts = map(self.export, rules)
            line = "&" + ",\\quad &&".join(parts)
            lines.append(line)
        rules_str = "\\\\ \n \t\t".join(lines)

        grammar_template = rf"""\begin{{figure}}
    \begin{{eqnarray*}}
        N & = & {self.export(grammar.non_terminals)} \\
        T & = & {self.export(grammar.non_terminals)} \\
        P & = & \left\{{ \begin{{aligned}}
                {rules_str}
                \end{{aligned}} \right\}} \\
        {grammar_name} & = & \{{N,T,P,{self.export(grammar.axiom)}\}}
    \end{{eqnarray*}}
\end{{figure}}"""
        return grammar_template

    @formatter(PhraseRule)
    def PhraseRule(self, rule):
        return rf"{self.export(rule.lhs)} \Rightarrow {self.export(rule.rhs)}"

    # scattered context grammars
    @formatter(ScatteredContextRule)
    def ScatteredContextRule(self, rule):
        lhs = r",\,".join(map(self.export, rule.lhs))
        rhs = r",\ ".join(map(self.export, rule.rhs))
        return rf"({lhs}) \Rightarrow ({rhs})"

    @formatter(PCGrammarSystem)
    def PCGrammarSystem(self, grammar, grammar_name="G"):
        components  = []
        for i, component in enumerate(grammar.components):
            component = self.export(component, grammar_name=f"C{i}")
            components.append(component)
        component_names = ", ".join([f"C{i}" for i in range(len(grammar.components))])
        components = "\n\n".join(components)
        communication_symbols = r"\{{" + ", ".join(map(self.export, grammar.communication_symbols)) + r"\}}"
        return rf"""{components}

\begin{{figure}}
    \begin{{eqnarray*}}
        {grammar_name} & = & \{{{communication_symbols}, {component_names}\}}
    \end{{eqnarray*}}
\end{{figure}}"""
