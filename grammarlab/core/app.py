
import argparse
import logging
from typing import Optional

from grammarlab.export import CliExport, CodeExport, GraphExport, LatexExport
from grammarlab.load import TextLoad

log = logging.getLogger("grammarlab.cli")


class App:
    """CLI interface for interacting with grammars.

    This class takes grammar as an argument and export various commands
    for working with this grammar to command line.

    Example:
        .. code-block:: python
            :caption: cf_a.py

            from grammarlab.core.app import App
            from grammarlab.grammars.grammars import CF

            G = CF({"S"}, {"a"}, [("S", "a"), ("S", "Sa")], "S")

            if __name__ == "__main__":
                App(G).run()

        .. code-block:: console

            $ python cf_a.py generate -d 3
            a
            aa
            aaa
            $ python cf_a.py generate -d 3 -s
            a
            S a
            a a
            S a a
            a a a
            S a a a
            $ python cf_a.py derivation_sequence -s "aaa"
            | Used Rule   | Sential Form   |
            |-------------+----------------|
            |             | S              |
            | S -> S a    | S a            |
            | S -> S a    | S a a          |
            | S -> a      | a a a          |
            $ python cf_a.py export --code
            from grammarlab.core.cli import App
            from grammarlab.grammars.grammars import RE

            N = {"S"}
            T = {"a"}
            S = "S"
            P = [
                ("S", "a"),
                ("S", "Sa"),
            ]

            G = RE(N, T, P, S)

            if __name__ == "__main__":
                App(G).run()

    """
    def __init__(self, grammar):
        self.grammar = grammar

        self.verbose = False
        self.latex_export = LatexExport()
        self.cli_export = CliExport()
        self.code_export = CodeExport()
        self.graph_export = GraphExport()

        self.text_load = TextLoad()

    def _parse_arguments(self):
        parser = argparse.ArgumentParser(
            prog="./grammarlab_script.py",
            description="Simulator for various types of grammars",
        )
        subparsers = parser.add_subparsers(dest="command")
        generate_parser = subparsers.add_parser("generate", help="Generate language of the grammar")
        generate_parser.add_argument("-d", "--depth", type=int, help="Max number of derivation steps")
        generate_parser.add_argument("-e", "--exact-depth", action="store_true", help="Generate only sentences with exact depth")
        generate_parser.add_argument("-s", "--show-sential-forms", action="store_true", help="Show sential forms")
        generate_parser.add_argument("-a", "--axiom", type=str, help="Start derivation from this sential form")
        generate_parser.add_argument("-x", "--delimiter", type=str, default="", help="Delimiter between symbols")
        generate_parser.add_argument("-v", "--verbose", action="store_true", help="Show all informations about configurations")

        derivation_sequence = subparsers.add_parser("derivation_sequence", help="Show derivation sequence for sentence")
        derivation_sequence.add_argument("-s", "--sentence", type=str, help="Sentence to derive")
        derivation_sequence.add_argument("-d", "--delimiter", type=str, default="", help="Delimiter between symbols")
        derivation_sequence.add_argument("-m", "--matches", type=int, default=1, help="Number of different derivation sequences (for ambiguous grammars)")

        ast = subparsers.add_parser("ast", help="Show AST for sentence")
        ast.add_argument("-s", "--sentence", type=str, help="Sentence to derive")
        ast.add_argument("-d", "--delimiter", type=str, default="", help="Delimiter between symbols")
        ast.add_argument("-m", "--matches", type=int, default=1, help="Number of different asts (for ambiguous grammars)")
        ast.add_argument("-f", "--filename", type=str, help="Filename to save ast to")

        export = subparsers.add_parser("export", help="Export grammar to various formats")
        export.add_argument("-c", "--code", action="store_true", help="Export grammar to python code")
        export.add_argument("-l", "--latex", action="store_true", help="Export grammar to latex")
        export.add_argument("-x", "--cli", action="store_true", help="Export grammar to cli")

        args = parser.parse_args()

        return args

    def run(self):
        """Run the application."""
        args = self._parse_arguments()
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
        max_steps: int = None,
        exact_depth: bool = False,
        only_sentences: bool = True,
        axiom: Optional[str] = None,
        delimiter: str = "",
        verbose: bool = False,
    ):
        """Generate sentences from the grammar.

        Args:
            max_steps: Maximum number of derivation steps.
            exact_depth: If True, only sentences with depth equal to max_steps will be generated.
            only_sentences: If True, only sentences will be printed (no sential forms).
            axiom: Axiom to start derivation from. If None, grammar's start symbol will be used.
            delimiter: Delimiter used to separate symbols in axiom
            verbose: If True, full configuration representation will be printed.
        Side effects:
            prints generated sentences to stdout.

        """
        if axiom:
            axiom = self.text_load.get_loader(self.grammar.configuration_class)(
                axiom, self.grammar, delimiter=delimiter
            )
        for configuration in self.grammar.derive(max_steps, exact_depth, only_sentences=only_sentences, axiom=axiom):
            print(self.cli_export.export(configuration if verbose else configuration.sential_form))

    def derivation_sequence(
        self,
        sentence: str = None,
        delimiter: str = "",
        matches: int = 1
    ):
        """Print derivation sequence for the given sentence.

        IDS strategy is used to find derivation sequences.
        If sentence is not generated by grammar app will print nothing and continue indefinitely.
        To stop the app press Ctrl+C.

        Args:
            sentence: Sentence to derive. Sentence is represented by string and deserialized by load module.
            delimiter: Delimiter used to separate symbols in sentence.
            matches: Number of derivation sequences to print. Useful when working with ambiguous grammars.
        Side effects:
            prints derivation sequence to stdout starting from axiom resulting in the given sentence.

        """
        configuration = self.text_load.get_loader(self.grammar.configuration_class)(
            sentence, self.grammar, delimiter=delimiter
        )
        for derived_configuration in self.grammar.parse(configuration, matches=matches):
            print(self.cli_export.export(derived_configuration.derivation_sequence()))

    def ast(self, filename, sentence=None, delimiter="", matches=1):
        """Visualize AST for the given sentence.

        Args:
            filename: Name of the file to save the visualization to.
            sentence: Sentence to derive. Sentence is represented by string and deserialized by load module.
            delimiter: Delimiter used to separate symbols in sentence.
            matches: Number of asts to create. Useful when working with ambiguous grammars.
        Side effects:
            saves ast visualization to file ./<filename>.pdf

        """
        filename = filename or "ast"
        configuration = self.text_load.get_loader(self.grammar.configuration_class)(
            sentence, self.grammar, delimiter=delimiter
        )
        for index, derived_configuration in enumerate(self.grammar.parse(configuration, matches=matches)):
            self.graph_export.export(
                derived_configuration,
                filename=filename if matches == 1 else f"{filename}_{index}"
            )

    def export(self, code, latex, cli):
        """Export grammar to the given format.

        Args:
            code: If True, export grammar to code representation.
            latex: If True, export grammar to latex representation.
            cli: If True, export grammar to cli representation.
        Raises:
            ValueError: If more than one export format is specified.
        Side effects:
            prints exported grammar to stdout.

        """
        if sum([code, latex, cli]) > 1:
            raise ValueError("Only one export format can be specified")
        if code:
            print(self.code_export.export(self))
        elif latex:
            print(self.latex_export.export(self.grammar))
        else:
            print(self.cli_export.export(self.grammar))
