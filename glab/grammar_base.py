from functools import wraps

class GrammarBase:
    def __init__(self):
        self.stack = []
        #self._derivation_sequence = []

    @classmethod
    def construct(cls, *args):
        pass

    def direct_derive(self, sential_form):
        pass

    def derive(self, max_steps, min_steps=None, sential_forms=False):
        self.stack = [self.direct_derive(self.axiom)]
        self._derivation_sequence = [self.axiom]
        while self.stack:
            try:
                next_sential_form = next(self.stack[-1])
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
            except StopIteration:
                self.stack.pop()
                self._derivation_sequence.pop()

    def derivation_sequence(self):
        return self._derivation_sequence


def restrictions(factory, *conditions):
    @wraps(factory)
    def wrapper(*args, **kwargs):
        grammar = factory(*args, **kwargs)
        for condition in conditions:
            condition(grammar)
        return grammar
    return wrapper
