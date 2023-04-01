
from glab.compact_definition import compact_string
import argparse
import logging


log = logging.getLogger("glab.cli")


class App:
    def __init__(self, grammar):
        self.grammar = grammar

        self.verbose = False

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            prog="Grammar Simulator",
            description="Simulator for various types of grammars",
        )
        parser.add_argument("-v", "--verbose", action="store_true")
        subparsers = parser.add_subparsers(dest="command")
        generate_parser = subparsers.add_parser("generate")
        generate_parser.add_argument("-d", "--depth", type=int)
        generate_parser.add_argument("-e", "--exact", action="store_true")
        generate_parser.add_argument("-s", "--show-sential-forms", action="store_true")
        generate_parser.add_argument("--enumerate", action="store_true")

        derivation_sequence = subparsers.add_parser("derivation_sequence")
        derivation_sequence.add_argument("-s", "--sentence", type=str)
        args = parser.parse_args()

        return args

    def run(self):
        args = self.parse_arguments()
        log.info(f"G-Lab started with args: {args}")

        self.verbose = args.verbose

        if self.verbose:
            log.info(f"Grammar: {self.grammar}")

        if args.command == "generate":
            self.generate(
                args.depth,
                min_steps=args.depth if args.exact else None,
                sential_forms=args.show_sential_forms,
                show_index=args.enumerate,
            )
        elif args.command == "derivation_sequence":
            self.derivation_sequence(args.sentence)

    def generate(self, max_steps=None, min_steps=None, sential_forms=False, show_index=False):
        index = 0
        for sentence in self.grammar.derive(max_steps, min_steps, sential_forms=sential_forms):
            index += 1
            if show_index:
                print(f"{index}: {sentence}")
            else:
                print(sentence)

    def derivation_sequence(self, sentence=None):
        sentence = compact_string(self.grammar.terminals, sentence)
        depth = 1
        found = False
        while not found:
            index = 0
            for s in self.grammar.derive(depth, depth):
                index += 1
                if sentence == s:
                    for sential_form in self.grammar.derivation_sequence():
                        print(sential_form)
                    print("Result sentence:")
                    print(s)
                    found = True
                    break
            depth += 1

