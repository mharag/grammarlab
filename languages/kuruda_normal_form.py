from grammars.grammars import CF
from glab.cli import App
from glab.alphabet import NonTerminal
from checkers.phrase_grammar_normal_forms import kuruda_normal_form_type_1

N = {"A", "B", "C", "D"}
T = {"a"}
P = [
    ("A", "CD"),
    ("A", "BC"),
    ("A", "a"),
    ("A", "")
]
S = "A"

#grammar = CS(N, T, P, S)

N = {"A", "B"}
T = {"a"}
P = [
    ("A", "a"),
    ("A", "AB"),
    ("B", "a"),
]
S = "A"

grammar = CF(N, T, P, S)
def max_one_B(sential_form):
    count = 0
    for symbol in sential_form:
        if symbol == NonTerminal("B"):
            count += 1
    return count <= 1

grammar.set_filter(max_one_B)

if __name__ == "__main__":
    App(grammar).run()
