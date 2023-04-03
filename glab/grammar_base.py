import logging
from functools import wraps

from glab.representation import Representable

log = logging.getLogger("glab.GrammarBase")


class ConfigurationBase(Representable):
    def __init__(self, data, parent=None, used_rule=None, affected=None):
        self.data = data
        self.parent = parent
        self.used_rule = used_rule
        self.affected = affected

    def __eq__(self, other):
        return isinstance(other, ConfigurationBase) and self.data == other.data

    @property
    def is_sentence(self):
        return self.data.is_sentence

    def copy(self):
        return self.__class__(
            self.data,
            self.parent,
            self.used_rule,
            self.affected,
        )


class ProductionBase(Representable):
    """Production of grammar

    This class represent one production of grammar.
    Every production is tried to be matched against current configuration and then applied.

    """

    def apply(self, configuration: ConfigurationBase):
        pass


class GrammarBase:
    """Formal grammar

    This class represents formal grammar. Grammar takes configuration and by using production generates
    new configurations

    Attributes:
        configuration_class (ConfigurationBase): Class representing one configuration
        production_class (ProductionBase): Class representing one production
    """

    configuration_class = ConfigurationBase
    production_class = ProductionBase

    def __init__(self):
        self.stack = []
        self.filters = []
        self._derivation_sequence = []

    def set_filter(self, func):
        log.info("Setting filter: %s.", func.__name__)
        self.filters.append(func)

    @property
    def axiom(self):
        raise NotImplementedError

    @classmethod
    def construct(cls, *args):
        raise NotImplementedError

    def direct_derive(self, sential_form):
        raise NotImplementedError

    def derive(self, max_steps, min_steps=None, sential_forms=False):
        log.info(
            "Derivation started. (max_steps=%s, min_steps=%s, sential_forms=%s)",
            max_steps, min_steps, sential_forms
        )
        log.info("Axiom: %s", self.axiom)

        self.stack = [self.direct_derive(self.axiom)]
        self._derivation_sequence = [self.axiom]
        while self.stack:
            next_sential_form = next(self.stack[-1], None)
            if next_sential_form is None:
                self.stack.pop()
                dead_sential_form = self._derivation_sequence.pop()
                log.debug("Dead: %s", dead_sential_form)
                continue

            valid = True
            for func in self.filters:
                if not func(next_sential_form):
                    valid = False
            if not valid:
                continue

            if not next_sential_form.is_sentence and sential_forms:
                yield next_sential_form

            if next_sential_form.is_sentence:
                if min_steps is None or len(self.stack) + 1 > min_steps:
                    yield next_sential_form
            elif len(self.stack) >= max_steps:
                continue
            else:
                self._derivation_sequence.append(next_sential_form)
                self.stack.append(self.direct_derive(next_sential_form))

    def derivation_sequence(self):
        return self._derivation_sequence


def restrictions(factory, *conditions):
    @wraps(factory)
    def wrapper(*args, **kwargs):
        grammar = factory(*args, **kwargs)
        for condition in conditions:
            log.debug("Imposing restriction: %s", condition.__name__)
            condition(grammar)
        return grammar
    return wrapper
