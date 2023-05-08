from glab.core.alphabet import Alphabet
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


def list_to_str(l):
    return "[" + ", ".join([f'"{t}"' for t in l]) + "]"


def set_to_str(l):
    return "{" + ", ".join([f'"{t}"' for t in l]) + "}"


def string_to_str(string, delimiter=""):
    return '"'+(delimiter.join(map(str, string)))+'"'


class CodeExport(Export):
    # Base objects
    @formatter(Alphabet)
    def alphabet(self, alphabet):
        return set_to_str(alphabet)

    @formatter("App")
    def app(self, app):
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
    def phrase_grammar(self, grammar, grammar_type="RE", grammar_name="G"):
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
            f"from glab.grammars.grammars import {grammar_type}"
        }
        return representation

    @formatter(PhraseRule)
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

    # Scattered context grammars
    @formatter(ScatteredContextGrammar)
    def scattered_context_grammar(self, grammar, grammar_name="G"):
        return self.phrase_grammar(grammar, grammar_type="SCG", grammar_name=grammar_name)

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

    # Parallel communicating grammar systems
    @formatter(PCGrammarSystem)
    def pc_grammar_system(self, grammar, grammar_name="G"):
        components = []
        imports = set()
        for i, component in enumerate(grammar.components):
            component = self.export(component, grammar_name=f"C{i}")
            components.append(component.content)
            imports = imports | component.imports
        components = "\n\n".join(components)
        component_names = ", ".join([f"C{i}" for i in range(len(grammar.components))])
        grammar_type = "NPC" if not grammar.returning else "PC"
        representation = CodeRepresentation(f"""\
{components}

{grammar_name} = {grammar_type}({list_to_str(grammar.communication_symbols)}, {component_names})
""")
        representation.imports = imports | {
            f"from glab.grammars.grammars import {grammar_type}"
        }
        return representation
