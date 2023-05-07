import functools
from typing import Generator, List

from glab.core.alphabet import String, Symbol
from glab.core.grammar_base import ConfigurationBase, GrammarBase
from glab.core.ast import Tree


class CommunicationRule(dict):
    """Communication rule is dynamic rule that maps communication symbols to current content of component."""


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

    @property
    def sential_form(self) -> String:
        """Sential form of configuration is sential form of first component."""
        return self.data[0].sential_form

    def __eq__(self, other: "PCConfiguration"):
        return isinstance(other, PCConfiguration) and self.data == other.data

    @property
    def order(self):
        """Order of configuration is number of components."""
        return len(self.data)

    def create_ast_root(self, depth) -> Tree:
        # create root nodes
        trees = [
            c.create_ast(depth=depth) for c in self.data
        ]
        return trees

    def apply_rule_to_ast(self, parent_trees: List[Tree], depth: int):
        for i, tree in enumerate(parent_trees):
            configuration = self.data[i]
            if isinstance(self.used_production, CommunicationRule):
                if configuration.used_production == "return":
                    new_node = tree.create_node(configuration.data[0], depth)
                    tree.frontier[0].add_children([new_node])
                    for parent in tree.frontier[1:]:
                        new_node.add_parent(parent)
                        parent.remove_from_frontier()
                elif configuration.used_production == "communication":
                    parents = [tree.frontier[x] for x in configuration.affected]
                    for parent in parents:
                        symbol = parent.data
                        rhs = self.used_production[symbol]
                        children = [tree.create_node(x, depth) for x in rhs]
                        parent.add_children(children)
            else:
                configuration.apply_rule_to_ast(tree, depth)

    def create_ast(self, depth: int = 0):
        """Create AST from configuration."""
        if not self.parent:
            parent_trees = self.create_ast_root(depth)
        else:
            parent_trees = self.parent.create_ast(depth=depth+1)
            self.apply_rule_to_ast(parent_trees, depth)

        if depth == 0:
            return functools.reduce(lambda a, b: a.merge(b), parent_trees)

        return parent_trees


class PCGrammarSystem(GrammarBase):
    """Parallel Comunicating Grammar System.
    """
    configuration_class = PCConfiguration

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
            # configuration is sentence, generation step is skipped
            return configuration, True
        if generator is None:
            # initialize generator
            generator = component.direct_derive(configuration)
            return next(generator, None), generator

        # get next configuration from generator
        next_sential_form, new_generator = next(generator, None), None
        if next_sential_form is None:
            # generator is empty, initialize new generator
            new_generator = component.direct_derive(configuration)
            next_sential_form = next(new_generator)
        return next_sential_form, new_generator

    def g_step(self, configuration: PCConfiguration) -> Generator[PCConfiguration, None, None]:
        """Perform generation step.

        All combinations of all possible derivations of all components are generated.
        If component is not able to derive, None is returned.
        For example if first component generate 3 configurations and second 2, 6 configurations are generated
        by grammar system.

        """
        # generators for each component
        generators = [None] * self.order
        next_configuration = [None] * self.order
        first_overflow = True
        while True:
            # generation works as odometer
            # when generator doesn't generate any new configuration (overflow)
            # it is reset, and generation continues with next component
            # first overflow of rightmost component is ignored
            # second overflow of rightmost component ends generation
            for i in range(self.order):
                # get next configuration from i-th component
                next_configuration[i], new_generator = self.get_next_configuration(
                    generators[i], self.components[i], configuration[i]
                )
                if next_configuration[i] is None:
                    # component cannot generate any configuration
                    return
                if new_generator:
                    # component has new generator
                    generators[i] = new_generator
                else:
                    # generator didn't overflow, no need to change other components
                    break
            else:
                if first_overflow:
                    first_overflow = False
                else:
                    break

            configurations = [
                self.components[i].configuration_class(
                    c.data.copy(),
                    c.parent,
                    c.used_production,
                    c.affected,
                    c.depth,
                )
                for i, c in enumerate(next_configuration)
            ]
            yield PCConfiguration(configurations, parent=configuration, depth=configuration.depth+1)

    def c_step(self, configuration):
        """Perform communication step."""
        copied = [False] * configuration.order
        new_configuration = [
            self.components[i].configuration_class(component.data.copy()) for i, component in enumerate(configuration)
        ]
        communication_rule = CommunicationRule()
        for i in range(configuration.order):
            affected = []
            sential_form = new_configuration[i].sential_form
            index = sential_form.index
            for communication_symbol in self.communication_symbols:
                positions = index.get(communication_symbol, None)
                if positions is None:
                    continue
                # source component
                referenced_component = self.communication_symbols.index(communication_symbol)
                if configuration[referenced_component].sential_form.index.keys() & self.communication_symbols:
                    # source component contains communication symbols, communication is not possible
                    continue
                communication_rule[communication_symbol] = configuration[referenced_component].sential_form
                copied[referenced_component] = True
                offset = 0
                affected.extend(positions)
                for position in positions:
                    sential_form.expand(position+offset, configuration[referenced_component].sential_form)
                    offset += len(configuration[referenced_component].sential_form) - 1

            new_configuration[i].affected = affected
            if affected:
                new_configuration[i].used_production = "communication"

        if True not in copied:
            # no component was copied, communication is not possible
            return

        if self.returning:
            # return copied components to initial state
            for i in range(configuration.order):
                if copied[i]:
                    new_configuration[i] = self.components[i].configuration_class(
                        String([self.components[i].start_symbol]),
                        used_production="return"
                    )

        yield PCConfiguration(
            new_configuration,
            parent=configuration,
            depth=configuration.depth+1,
            used_production=communication_rule
        )

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
    for component in grammar.components[1:]:
        for non_terminal in component.non_terminals:
            if non_terminal in grammar.communication_symbols:
                raise ValueError("In centralized grammar can only main component contain comunication symbols!")
