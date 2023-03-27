class Grammar:
    def direct_derive(self, sential_form):
        pass

    def derive(self, max_depth):
        stack = [self.direct_derive(self.axiom)]
        while stack:
            try:
                next_sential_form = next(stack[-1])
                if next_sential_form.is_sentence:
                    yield next_sential_form
                elif len(stack) >= max_depth:
                    continue
                else:
                    stack.append(self.direct_derive(next_sential_form))
            except Exception:
                stack.pop()
