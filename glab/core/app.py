
import argparse
import logging

from glab.core.visualize_ast import visualize_ast
from glab.export import CliExport, CodeExport, LatexExport
from glab.load import TextLoad

log = logging.getLogger("glab.cli")


class App:
    def __init__(self, grammar):
        self.grammar = grammar

        self.verbose = False
        self.latex_export = LatexExport()
        self.cli_export = CliExport()
        self.code_export = CodeExport()

        self.text_load = TextLoad()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            prog="Grammar Simulator",
            description="Simulator for various types of grammars",
        )
        subparsers = parser.add_subparsers(dest="command")
        generate_parser = subparsers.add_parser("generate")
        generate_parser.add_argument("-d", "--depth", type=int)
        generate_parser.add_argument("-e", "--exact-depth", action="store_true")
        generate_parser.add_argument("-s", "--show-sential-forms", action="store_true")
        generate_parser.add_argument("--enumerate", action="store_true")
        generate_parser.add_argument("-a", "--axiom", type=str)
        generate_parser.add_argument("-x", "--delimiter", type=str, default="")
        generate_parser.add_argument("-v", "--verbose", action="store_true")

        derivation_sequence = subparsers.add_parser("derivation_sequence")
        derivation_sequence.add_argument("-s", "--sentence", type=str)
        derivation_sequence.add_argument("-d", "--delimiter", type=str, default="")
        derivation_sequence.add_argument("-m", "--matches", type=int, default=1)

        ast = subparsers.add_parser("ast")
        ast.add_argument("-s", "--sentence", type=str)
        ast.add_argument("-d", "--delimiter", type=str, default="")
        ast.add_argument("-m", "--matches", type=int, default=1)
        ast.add_argument("-f", "--filename", type=str)

        export = subparsers.add_parser("export")
        export.add_argument("-c", "--code", action="store_true")
        export.add_argument("-l", "--latex", action="store_true")
        export.add_argument("-x", "--cli", action="store_true")

        args = parser.parse_args()

        return args

    def run(self):
        args = self.parse_arguments()
        log.info("G-Lab started with args: %s", args)

        if args.command == "generate":
            self.generate(
                args.depth,
                exact_depth=args.exact_depth,
                only_sentences=not args.show_sential_forms,
                axiom=args.axiom,
                delimiter=args.delimiter,
                verbose=args.verbose,
            )
        elif args.command == "derivation_sequence":
            self.derivation_sequence(args.sentence, args.delimiter, args.matches)
        elif args.command == "ast":
            self.ast(args.filename, args.sentence, args.delimiter, args.matches)
        elif args.command == "export":
            self.export(args.code, args.latex, args.cli)

    def generate(
        self,
        max_steps=None,
        exact_depth=False,
        only_sentences=True,
        axiom=None,
        delimiter="",
        verbose=False
    ):
        if axiom:
            axiom = self.text_load.get_loader(self.grammar.configuration_class)(
                axiom, self.grammar, delimiter=delimiter
            )
        for configuration in self.grammar.derive(max_steps, exact_depth, only_sentences=only_sentences, axiom=axiom):
            print(self.cli_export.export(configuration if verbose else configuration.sential_form))

    def derivation_sequence(self, sentence=None, delimiter="", matches=1):
        configuration = self.text_load.get_loader(self.grammar.configuration_class)(
            sentence, self.grammar, delimiter=delimiter
        )
        for derived_configuration in self.grammar.parse(configuration, matches=matches):
            print(self.cli_export.export(derived_configuration.derivation_sequence()))

    def ast(self, filename, sentence=None, delimiter="", matches=1):
        configuration = self.text_load.get_loader(self.grammar.configuration_class)(
            sentence, self.grammar, delimiter=delimiter
        )
        for derived_configuration in self.grammar.parse(configuration, matches=matches):
            ast = derived_configuration.create_ast()
            visualize_ast(ast, filename)

    def export(self, code, latex, cli):
        if sum([code, latex, cli]) > 1:
            raise ValueError("Only one export format can be specified")
        if code:
            print(self.code_export.export(self))
        elif latex:
            print(self.latex_export.export(self.grammar))
        else:
            print(self.cli_export.export(self.grammar))
