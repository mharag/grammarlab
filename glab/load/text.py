from glab.core.alphabet import Alphabet, String
from glab.grammars.pc_grammar_system import PCConfiguration, PCGrammarSystem
from glab.grammars.phrase_grammar import PhraseConfiguration, PhraseGrammar
from glab.load.load import Load, loader


class TextLoad(Load):
    @loader(String)
    def string(self, cls, string: str, alphabet: Alphabet, delimiter=""):
        result = []
        if delimiter:
            string = string.split(delimiter)
        for symbol in string:
            result.append(alphabet.lookup(symbol))
        return cls(result)

    @loader(PhraseConfiguration)
    def phrase_configuration(self, cls, raw_configuration, grammar: PhraseGrammar, delimiter=""):
        """Deserialize configuration from string.

        Example of string representation:
            ABCD
            aaaAAAA
            S_G,B_G,C_G,D_G (delimeter is ',')

        Args:
            raw_configuration: String representation of configuration.
            grammar: Grammar that this configuration belongs to.
            delimiter: Delimiter used to separate symbols of sential form.

        Returns:
            PhraseConfiguration instance.

        """
        alphabet = grammar.non_terminals.union(grammar.terminals)
        return cls(self.load(String, raw_configuration, alphabet, delimiter))

    @loader(PCConfiguration)
    def pc_configuration(self, cls, raw_configuration, grammar: PCGrammarSystem, delimiter):
        """Deserialize configuration from string.

        Configurations of components are separated by two delimiters.

        Example of string representation:
            A B C D  A B C D  A B C D

        """
        if not delimiter:
            raise ValueError("Delimiter cannot be empty string.")

        # split configurations of components
        raw_configurations = raw_configuration.split(delimiter * 2)
        configurations = []
        for i, configuration in enumerate(raw_configurations):
            component = grammar.components[i]
            # deserialize component configurations
            configurations.append(
                self.load(component.configuration_class, configuration, component, delimiter)
            )
        return cls(configurations)
