from glab.alphabet import N, T, A, S
from glab.grammar_base import GrammarBase
from glab.compact_definition import compact_communication_symbols


class Configuration:
    def __init__(self, configuration: list[S]):
        self.configuration = configuration

    def __getitem__(self, item):
        return self.configuration[item]

    def __repr__(self):
        sential_forms = ", ".join(str(sential_form) for sential_form in self.configuration)
        return f"Configuration({sential_forms})"

    def __str__(self):
        return str(self.configuration[0])
    def __eq__(self, other):
        return type(self) == type(other) and self.configuration == other.configuration

    @property
    def is_sentence(self):
        return self.configuration[0].is_sentence

    @property
    def order(self):
        return len(self.configuration)



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

    def communication(self, configuration):
        for sential_form in configuration:
            for symbol in sential_form.symbols:
                if symbol in self.communication_symbols:
                    return True
        return False


    @property
    def axiom(self):
        return Configuration([c.axiom for c in self.components])

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

            yield Configuration([x.copy() for x in next_configuration])

    def c_step(self, configuration):
        copied = [False] * configuration.order
        new_configuration = [sential_form.copy() for sential_form in configuration]
        for i in range(configuration.order):
            sential_form = new_configuration[i]
            index = sential_form.create_index(self.communication_symbols)
            for communication_symbol, positions in index.items():
                referenced_component = self.communication_symbols.index(communication_symbol)
                if configuration[referenced_component].create_index(self.communication_symbols):
                    continue
                copied[referenced_component] = True
                offset = 0
                for position in positions:
                    sential_form.expand(position+offset, configuration[referenced_component])
                    offset += len(configuration[referenced_component]) - 1

        if True not in copied:
            return

        if self.returning:
            for i in range(configuration.order):
                if copied[i]:
                    new_configuration[i] = S([self.components[i].start_symbol])

        yield Configuration(new_configuration)

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
