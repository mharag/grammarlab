
import argparse
import logging

from glab.table import create_table
from glab.visualize_ast import visualize_ast

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
        generate_parser.add_argument("-e", "--exact-depth", action="store_true")
        generate_parser.add_argument("-s", "--show-sential-forms", action="store_true")
        generate_parser.add_argument("--enumerate", action="store_true")

        derivation_sequence = subparsers.add_parser("derivation_sequence")
        derivation_sequence.add_argument("-s", "--sentence", type=str)
        derivation_sequence.add_argument("-d", "--delimiter", type=str, default="")
        derivation_sequence.add_argument("-m", "--matches", type=int, default=1)
        args = parser.parse_args()

        return args

    def run(self):
        args = self.parse_arguments()
        log.info("G-Lab started with args: %s", args)

        self.verbose = args.verbose

        if self.verbose:
            log.info("Grammar: %s", self.grammar.cli_output())

        if args.command == "generate":
            self.generate(
                args.depth,
                exact_depth=args.exact_depth,
                only_sentences=not args.show_sential_forms,
            )
        elif args.command == "derivation_sequence":
            self.derivation_sequence(args.sentence, args.delimiter, args.matches)

    def generate(self, max_steps=None, exact_depth=False, only_sentences=True):
        sentences = []
        for sentence in self.grammar.derive(max_steps, exact_depth, only_sentences=only_sentences):
            sentences.append(sentence)
        print(create_table(sentences))

    def derivation_sequence(self, sentence=None, delimiter="", matches=1):
        sentence = self.grammar.parse_configuration(sentence, delimiter=delimiter)
        depth = 1
        while matches:
            index = 0
            for s in self.grammar.derive(depth, exact_depth=True):
                index += 1
                if sentence == s:
                    print(create_table(list(s.derivation_sequence())))
                    ast = s.create_ast()
                    visualize_ast(ast)
                    matches -= 1
                    if not matches:
                        break
            depth += 1
