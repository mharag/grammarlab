import functools
from typing import List

from glab.alphabet import String, Symbol
from glab.compact_definition import compact_communication_symbols
from glab.grammar_base import ConfigurationBase, GrammarBase


class CommunicationRule(dict):
    pass


class PCConfiguration(ConfigurationBase):
    """Configuration for PC grammar system.
    """

    def __getitem__(self, item: int) -> ConfigurationBase:
        """Get component configuration by index."""
        if item < 0 or item >= len(self.data):
            raise IndexError
        return self.data[item]

    def __getattr__(self, attr: str) -> ConfigurationBase:
        """Get component configuration by name."""
        if attr.startswith("component_"):
            index = int(attr.replace("component_", ""))
            return self.data[index]
        raise AttributeError

    def __repr__(self):
        sential_forms = ", ".join(str(sential_form) for sential_form in self.data)
        return f"Configuration({sential_forms})"

    def __str__(self):
        return "  ".join([str(component) for component in self.data])

    @classmethod
    def deserialize(cls, grammar: "PCGrammarSystem", representation: str, delimiter: str):
        """Deserialize configuration from string.

        Configurations of components are separated by two delimiters.

        Example of string representation:
            A B C D  A B C D  A B C D

        """

        # split configurations of components
        representations = representation.split(delimiter * 2)
        configurations = []
        for i, configuration in enumerate(representations):
            component = grammar.components[i]
            # deserialize component configurations
            configurations.append(component.configuration_class.deserialize(component, configuration, delimiter))
        return PCConfiguration(configurations)

    @property
    def sential_form(self) -> String:
        """Sential form of configuration is sential form of first component."""
        return self.data[0].sential_form

    def cli_output(self):
        return "  ".join([component.cli_output() for component in self.data])

    def __eq__(self, other: "PCConfiguration"):
        return isinstance(other, PCConfiguration) and self.data == other.data

    @property
    def order(self):
        """Order of configuration is number of components."""
        return len(self.data)

    def create_ast(self):
        """Create AST from configuration."""
        components_ast = [x.create_ast() for x in self.data]
        return functools.reduce(lambda a, b: a.merge(b), components_ast)


class PCGrammarSystem(GrammarBase):
    """Parallel Comunicating Grammar System.
    """
    def __init__(self,
        comumunication_symbols: List[Symbol],
        components: List[GrammarBase],
        returning: bool = True
    ):
        """Create PC grammar system.
        Args:
            comumunication_symbols: Symbols that are used for communication between components. i-th points to i-th component.
            components: List of components.
            centralized: If True, only fist component can initialize communication.
            returning: If True, component is returned to its initial state after communication.
        Returns:
            PCGrammarSystem
        """
        super().__init__()
        self.components = components
        self.returning = returning
        self.communication_symbols = comumunication_symbols

    @classmethod
    def deserialize(cls, communication_symbols: List[Symbol], *components: List[GrammarBase],  returning: bool = True):
        """Deserialize PC grammar system.

        Args:
            communication_symbols: List of communication symbols.
            components: List of components.
            returning: If True, component is returned to its initial state after communication.

        Returns:
            PCGrammarSystem

        """
        communication_symbols = compact_communication_symbols(communication_symbols)
        return cls(
            comumunication_symbols=communication_symbols,
            components=components,
            returning=returning,
        )

    def __str__(self):
        components = "\n".join(f"Component {i+1}:\n{component}" for i, component in enumerate(self.components))
        return f"""PC grammar system
Comunication symbols: {self.communication_symbols}
{components}
"""

    def communication(self, configuration):
        """Check if configuration contains communication symbol."""
        for sential_form in configuration.data:
            for symbol in sential_form.data:
                if symbol in self.communication_symbols:
                    return True
        return False


    @property
    def axiom(self):
        return PCConfiguration([c.axiom for c in self.components])

    @property
    def order(self):
        """Order of grammar system is number of components."""
        return len(self.components)

    def get_next_configuration(self, generator, component, configuration):
        if configuration.sential_form.is_sentence:
            return configuration, True
        if generator is None:
            generator = component.direct_derive(configuration)
            return next(generator, None), generator

        next_sential_form, new_generator = next(generator, None), None
        if next_sential_form is None:
            new_generator = component.direct_derive(configuration)
            next_sential_form = next(new_generator)
        return next_sential_form, new_generator

    def g_step(self, configuration):
        generators = [None] * self.order
        next_configuration = [None] * self.order
        first_overflow = True
        while True:
            for i in range(self.order):
                next_configuration[i], new_generator = self.get_next_configuration(
                    generators[i], self.components[i], configuration[i]
                )
                if next_configuration[i] is None:
                    return
                if new_generator:
                    generators[i] = new_generator
                else:
                    break
            else:
                if first_overflow:
                    first_overflow = False
                else:
                    break

            yield PCConfiguration([x.copy() for x in next_configuration], parent=configuration, depth=configuration.depth+1)

    def c_step(self, configuration):
        """Perform communication step."""
        copied = [False] * configuration.order
        new_configuration = [sential_form.copy() for sential_form in configuration]
        for i in range(configuration.order):
            communication_rule = CommunicationRule()
            affected = []
            sential_form = new_configuration[i].sential_form
            index = sential_form.create_index(self.communication_symbols)
            for communication_symbol, positions in index.items():
                referenced_component = self.communication_symbols.index(communication_symbol)
                if configuration[referenced_component].sential_form.create_index(self.communication_symbols):
                    continue
                communication_rule[communication_symbol] = configuration[referenced_component].sential_form
                copied[referenced_component] = True
                offset = 0
                affected.extend(positions)
                for position in positions:
                    sential_form.expand(position+offset, configuration[referenced_component].sential_form)
                    offset += len(configuration[referenced_component].sential_form) - 1
            new_configuration[i].used_production = communication_rule
            new_configuration[i].affected = affected
            new_configuration[i].parent = configuration[i]

        if True not in copied:
            return

        if self.returning:
            for i in range(configuration.order):
                if copied[i]:
                    new_configuration[i] = self.components[i].configuration_class(
                        String([self.components[i].start_symbol]),
                        parent=configuration[i]
                    )

        yield PCConfiguration(new_configuration, parent=configuration, depth=configuration.depth+1)

    def direct_derive(self, configuration):
        """Perform direct derivation on configuration."""
        # if configuration contains communication symbol perform c_step else perform g_step
        if self.communication(configuration):
            for sential_form in self.c_step(configuration):
                yield sential_form
        else:
            for sential_form in self.g_step(configuration):
                yield sential_form


def centralized_pc(grammar):
    for component in grammar[1:]:
        for non_terminal in component.non_terminals:
            if non_terminal in grammar.communication_symbols:
                raise ValueError("In centralized grammar can only main component contain comunication symbols!")
