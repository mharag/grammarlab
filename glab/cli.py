
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

        ast = subparsers.add_parser("ast")
        ast.add_argument("-s", "--sentence", type=str)
        ast.add_argument("-d", "--delimiter", type=str, default="")
        ast.add_argument("-m", "--matches", type=int, default=1)
        ast.add_argument("-f", "--filename", type=str)
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
        elif args.command == "ast":
            self.ast(args.filename, args.sentence, args.delimiter, args.matches)

    def generate(self, max_steps=None, exact_depth=False, only_sentences=True):
        for configuration in self.grammar.derive(max_steps, exact_depth, only_sentences=only_sentences):
            print(configuration.sential_form)

    def derivation_sequence(self, sentence=None, delimiter="", matches=1):
        configuration = self.grammar.configuration_class.deserialize(self.grammar, sentence, delimiter=delimiter)
        for derived_configuration in self.grammar.parse(configuration, matches=matches):
            print(create_table(list(derived_configuration.derivation_sequence())))

    def ast(self, filename, sentence=None, delimiter="", matches=1):
        configuration = self.grammar.configuration_class.deserialize(self.grammar, sentence, delimiter=delimiter)
        for derived_configuration in self.grammar.parse(configuration, matches=matches):
            ast = derived_configuration.create_ast()
            visualize_ast(ast, filename)
