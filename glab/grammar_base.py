from functools import wraps
import logging
from glab.alphabet import N


log = logging.getLogger("glab.GrammarBase")


class GrammarBase:
    def __init__(self):
        self.stack = []
        self.filters = []
        self._derivation_sequence = []

    def set_filter(self, func):
        log.info(f"Setting filter: {func.__name__}.")
        self.filters.append(func)

    @classmethod
    def construct(cls, *args):
        raise NotImplemented

    def direct_derive(self, sential_form):
        raise NotImplemented

    def derive(self, max_steps, min_steps=None, sential_forms=False):
        log.info(
            f"Derivation started. (max_steps={max_steps}, min_steps={min_steps}, sential_forms={sential_forms})"
        )
        log.info(f"Axiom: {self.axiom}")

        self.stack = [self.direct_derive(self.axiom)]
        self._derivation_sequence = [self.axiom]
        while self.stack:
            next_sential_form = next(self.stack[-1], None)
            if next_sential_form is None:
                self.stack.pop()
                dead_sential_form = self._derivation_sequence.pop()
                log.debug(f"Dead: {dead_sential_form}")
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
            log.debug(f"Imposing restriction: {condition.__name__}")
            condition(grammar)
        return grammar
    return wrapper
