from glab.core.alphabet import Alphabet, String, Symbol
from glab.export.export import Export, formatter
from glab.grammars.pc_grammar_system import PCGrammarSystem
from glab.grammars.phrase_grammar import PhraseGrammar, PhraseRule
from glab.grammars.scattered_context_grammar import (ScatteredContextGrammar,
                                                     ScatteredContextRule)


class CodeRepresentation:
    def __init__(self, content):
        self.content = content
        self.imports = set()

    def __str__(self):
        imports_str = "\n".join(self.imports)

        return f"""{imports_str}

{self.content}"""


class CodeExport(Export):
    # Base objects
    @formatter(String)
    def String(self, string, force_list=False):
        """
        .. code-block:: python

            "abc"
            ["a_1", "b_2", "c_3"]

        """
        if force_list or any(len(symbol.id) > 1 for symbol in string):
            return "[" + ", ".join([f'"{t}"' for t in string]) + "]"
        else:
            return '"'+("".join(map(str, string)))+'"'

    @formatter(Alphabet)
    def Alphabet(self, alphabet):
        """
        .. code-block:: python

            {"S", "A", "B", "C", "a", "b", "c"}

        """
        return "{" + ", ".join([f'"{t}"' for t in alphabet]) + "}"

    @formatter(Symbol)
    def Symbol(self, symbol):
        """
        .. code-block:: python

            "S"

        """
        return '"'+symbol.id+'"'

    @formatter("App")
    def App(self, app):
        """
        .. code-block:: python

            from glab.core.app import App
            from glab.grammars import CF

            G = CF(...)

            if __name__ == "__main__":
                App(G).run()

        """
        grammar = self.export(app.grammar, grammar_name="G")
        representation = CodeRepresentation(f"""{grammar.content}
if __name__ == "__main__":
    App(G).run()
""")
        representation.imports.add("from glab.core.cli import App")
        representation.imports.update(grammar.imports)
        return representation

    # Phrase grammars
    @formatter(PhraseGrammar)
    def PhraseGrammar(self, grammar, grammar_type="RE", grammar_name="G"):
        """
        .. code-block:: python

            from glab.grammars.grammars import RE

            N = {"S", "A", "B"}
            T = {"a"}
            S = "S"
            P = [
                ("S", "a"),
                ("S", "AB"),
            ]

            G = RE(N, T, P, S)

        """
        rules = "\n".join([f"    {self.export(rule)}," for rule in grammar.rules])
        representation = CodeRepresentation(f"""\
N = {self.export(grammar.non_terminals)}
T = {self.export(grammar.terminals)}
S = "{str(grammar.start_symbol)}"
P = [
{rules}
]

{grammar_name} = {grammar_type}(N, T, P, S)
""")
        representation.imports = {
            f"from glab.grammars import {grammar_type}"
        }
        return representation

    @formatter(PhraseRule)
    def PhraseRule(self, rule):
        """
        .. code-block:: python

            ("S", "abc")

        """
        return f"({self.export(rule.lhs)}, {self.export(rule.rhs)})"

    # Scattered context grammars
    @formatter(ScatteredContextGrammar)
    def ScatteredContextGrammar(self, grammar, grammar_name="G"):
        """
        .. code-block:: python

            from glab.grammars import SCG

            N = {"S", "A", "B"}
            T = {"a"}
            S = "S"
            P = [
                (["S", "A"], ["B", "A"]),
            ]

            G = SCG(N, T, P, S)

        """
        return self.phrase_grammar(grammar, grammar_type="SCG", grammar_name=grammar_name)

    @formatter(ScatteredContextRule)
    def ScatteredContextRule(self, rule):
        """
        .. code-block:: python

            (["S", "A"], ["B", "A"])

        """
        lhs = "[" + ", ".join(map(self.export, rule.lhs)) + "]"
        rhs = []
        for string in rule.rhs:
            rhs.append(self.export(string))
        rhs = "[" + (", ".join(rhs)) + "]"
        return f"({lhs}, {rhs})"

    # Parallel communicating grammar systems
    @formatter(PCGrammarSystem)
    def PCGrammarSystem(self, grammar, grammar_name="G"):
        """
        .. code-block:: python

            from glab.grammars import PC
            from glab.grammars import CF

            C_1 = CF(...)
            C_2 = CF(...)
            C_3 = CF(...)

            G = PC(["a", "b", "c"], C_1, C_2, C_3)

        """
        components = []
        imports = set()
        for i, component in enumerate(grammar.components):
            component = self.export(component, grammar_name=f"C{i}")
            components.append(component.content)
            imports = imports | component.imports
        components = "\n\n".join(components)
        component_names = ", ".join([f"C{i}" for i in range(len(grammar.components))])
        grammar_type = "NPC" if not grammar.returning else "PC"
        communication_symbols = "[" + ", ".join([f'"{t}"' for t in grammar.communication_symbols]) + "]"

        representation = CodeRepresentation(f"""\
{components}

{grammar_name} = {grammar_type}({communication_symbols}, {component_names})
""")
        representation.imports = imports | {
            f"from glab.grammars.grammars import {grammar_type}"
        }
        return representation
