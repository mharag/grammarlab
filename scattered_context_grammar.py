
class ScatteredContextRule:
    def __init__(self, lhs: list[Nonterminal], rhs: list):
        if len(lhs) != len(rhs):
            raise ValueError(f"Different order of right and left side!")


class ScatteredContextGrammar:
