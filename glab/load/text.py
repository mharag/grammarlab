from glab.core.alphabet import Alphabet, String
from glab.grammars.pc_grammar_system import PCConfiguration, PCGrammarSystem
from glab.grammars.phrase_grammar import PhraseConfiguration, PhraseGrammar
from glab.load.load import Load, loader


class TextLoad(Load):
    """Text deserializer.

    TextLoad is used to deserialize objects from text representation.

    """

    @loader(String)
    def String(self, cls, string: str, alphabet: Alphabet, delimiter="") -> String:
        """Deserialize string from string.

        Args:
            string: String representation of string.
            alphabet: Alphabet that this string belongs to.
            delimiter: Delimiter used to separate symbols of string.

        Returns:
            String instance.

        """
        result = []
        if delimiter:
            string = string.split(delimiter)
        for symbol in string:
            result.append(alphabet.lookup(symbol))
        return cls(result)

    @loader(PhraseConfiguration)
    def PhraseConfiguration(self, cls, raw_configuration, grammar: PhraseGrammar, delimiter="") -> PhraseConfiguration:
        """Deserialize phrase configuration from string.

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
    def PCConfiguration(self, cls, raw_configuration, grammar: PCGrammarSystem, delimiter) -> PCConfiguration:
        """Deserialize configuration from string.

        Configurations of components are separated by two delimiters.

        Args:
            raw_configuration: String representation of configuration.
            grammar: Grammar that this configuration belongs to.
            delimiter: Delimiter used to separate symbols and configurations of components.

        Returns:
            PCConfiguration.

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
