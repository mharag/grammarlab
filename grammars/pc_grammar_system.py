from glab.alphabet import N, T, A, S
from glab.grammar_base import GrammarBase, ConfigurationBase
from glab.compact_definition import compact_communication_symbols
import functools


class CommunicationRule(dict):
    pass


class PCConfiguration(ConfigurationBase):
    def __getitem__(self, item):
        return self.data[item]

    def __repr__(self):
        sential_forms = ", ".join(str(sential_form) for sential_form in self.data)
        return f"Configuration({sential_forms})"

    def __str__(self):
        return "  ".join([str(component) for component in self.data])

    def __eq__(self, other):
        return type(self) == type(other) and self.data == other.data

    @property
    def is_sentence(self):
        return self.data[0].is_sentence

    @property
    def order(self):
        return len(self.data)

    def create_ast(self, depth=0):
        components_ast = [x.pc_create_ast() for x in self.data]
        return functools.reduce(lambda a, b: a.merge(b), components_ast)


class PCGrammarSystem(GrammarBase):
    def __init__(self, comumunication_symbols, components, centralized=False, returning=True):
        super().__init__()
        self.components = components
        self.centralized = centralized
        self.returning = returning

        self.communication_symbols = comumunication_symbols

    @classmethod
    def construct(cls, communication_symbols, *components,  returning=True):
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
        for sential_form in configuration.data:
            for symbol in sential_form.data:
                if symbol in self.communication_symbols:
                    return True
        return False


    @property
    def axiom(self):
        return PCConfiguration([c.axiom for c in self.components])

    def parse_configuration(self, representation, delimiter):
        components = representation.split(delimiter * 2)
        configurations = []
        for i, component in enumerate(components):
            configurations.append(self.components[i].parse_configuration(component, delimiter))
        return PCConfiguration(configurations)

    @property
    def order(self):
        return len(self.components)

    def get_next_sential_form(self, generator, component, sential_form):
        if sential_form.is_sentence:
            return sential_form, True
        if generator is None:
            generator = component.direct_derive(sential_form)
            return next(generator, None), generator

        next_sential_form, new_generator = next(generator, None), None
        if next_sential_form is None:
            new_generator = component.direct_derive(sential_form)
            next_sential_form = next(new_generator)
        return next_sential_form, new_generator

    def g_step(self, configuration):
        generators = [None] * self.order
        next_configuration = [None] * self.order
        first_overflow = True
        while True:
            for i in range(self.order):
                next_configuration[i], new_generator = self.get_next_sential_form(
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

            yield PCConfiguration(next_configuration)

    def c_step(self, configuration):
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
            new_configuration[i].used_rule = communication_rule
            new_configuration[i].affected = affected
            new_configuration[i].parent = configuration[i]


        if True not in copied:
            return

        if self.returning:
            for i in range(configuration.order):
                if copied[i]:
                    new_configuration[i] = self.components[i].configuration(
                        S([self.components[i].start_symbol]),
                        parent=configuration[i]
                    )

        yield PCConfiguration(new_configuration)

    def direct_derive(self, configuration):
        if self.communication(configuration):
            for sential_form in self.c_step(configuration):
                yield sential_form
        else:
            for sential_form in self.g_step(configuration):
                yield sential_form


def centralized(grammar):
    for component in grammar[1:]:
        for non_terminal in component.non_terminals:
            if type(non_terminal) == C:
                raise ValueError(f"In centralized grammar can only main component contain comunication symbols!")
