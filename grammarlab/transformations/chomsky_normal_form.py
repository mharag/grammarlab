from itertools import product
from typing import Set

from rich.console import Console
from rich.panel import Panel

from grammarlab.core.common import Alphabet, NonTerminal, String, Symbol, epsilon
from grammarlab.export.cli import CliExport
from grammarlab.grammars import ContextFreeRule, PhraseGrammar

console = Console()
cli_export = CliExport()


def find_generating_symbols(grammar: PhraseGrammar) -> Set[Symbol]:
    """ Find all generating symbols in grammar
    Args:
        grammar: Context-free grammar

    Returns:
        Set of generating symbols

    """
    console.rule("[bold]Finding generating symbols in grammar", style="grey")
    generating_symbols = set(grammar.terminals)
    console.print("[bold]- Step 0:")
    console.print(f"    Teminals added to generating symbols: {cli_export.export(generating_symbols)}")
    unknown = set(grammar.non_terminals)

    changed = True
    step = 0
    while changed:
        step += 1
        console.print(f"[bold]- Step {step}:")
        changed = False
        for rule in grammar.rules:
            if rule.lhs[0] not in generating_symbols:
                if all(symbol in generating_symbols for symbol in rule.rhs):
                    generating_symbols.add(rule.lhs[0])
                    unknown.remove(rule.lhs[0])
                    changed = True
                    console.print(
                        f"    Symbol {cli_export.export(rule.lhs[0])} "
                        f"added to generating symbols based on rule {cli_export.export(rule)}"
                    )
        console.print(f"    Generating symbols: {cli_export.export(generating_symbols)}")
    console.print()
    console.print(f"[bold]All generating symbols found: {cli_export.export(generating_symbols)}")
    console.rule(style="gray")
    return generating_symbols


def find_reachable_symbols(grammar: PhraseGrammar) -> Set[Symbol]:
    """ Find all reachable symbols in grammar

    Args:
        grammar: Context-free grammar

    Returns:
        Set of generating symbols

    """
    console.rule("[bold]Finding reachable symbols in grammar", style="grey")
    reachable_symbols = {grammar.start_symbol}
    console.print("[bold]- Step 0:")
    console.print(f"    Start symbol added to reachable symbols: {cli_export.export(reachable_symbols)}")
    unknown = {
        symbol for symbol in
        grammar.non_terminals.union(grammar.terminals) if symbol not in reachable_symbols
    }

    changed = True
    step = 0
    while changed:
        step += 1
        console.print(f"[bold]- Step {step}:")
        changed = False
        for rule in grammar.rules:
            if rule.lhs[0] in reachable_symbols:
                for symbol in rule.rhs:
                    if symbol not in reachable_symbols:
                        reachable_symbols.add(symbol)
                        unknown.remove(symbol)
                        changed = True
                        console.print(
                            f"    Symbol {cli_export.export(symbol)} "
                            f"added to reachable symbols based on rule {cli_export.export(rule)}"
                        )
        console.print(f"    Reachable symbols: {cli_export.export(reachable_symbols)}")
    console.print(f"[bold]All reachable symbols found: {cli_export.export(reachable_symbols)}")
    console.rule(style="gray")
    return reachable_symbols


def find_nullable_symbols(grammar: PhraseGrammar) -> PhraseGrammar:
    """ Find all nullable symbols in grammar

    Args:
        grammar: Phrase grammar

    Returns:
        Set of nullable symbols

    """
    console.rule("[bold]Finding nullable symbols in grammar", style="grey")
    nullable_symbols = set()

    changed = True
    step = 0
    while changed:
        step += 1
        console.print(f"[bold]- Step {step}:")
        changed = False
        for rule in grammar.rules:
            if all(symbol in nullable_symbols for symbol in rule.rhs):
                if rule.lhs[0] not in nullable_symbols:
                    nullable_symbols.add(rule.lhs[0])
                    changed = True
                    console.print(
                        f"    Symbol {cli_export.export(rule.lhs[0])} "
                        f"added to nullable symbols based on rule {cli_export.export(rule)}"
                    )
        console.print(f"    Nullable symbols: {cli_export.export(nullable_symbols)}")

    console.print(f"[bold]All nullable symbols found: {cli_export.export(nullable_symbols)}")
    console.rule(style="gray")
    return nullable_symbols


def remove_epsilon_rules(grammar: PhraseGrammar) -> PhraseGrammar:
    """ Remove epsilon rules from grammar

    Args:
        grammar: Phrase grammar

    Returns:
        New phrase grammar without epsilon rules

    """
    console.rule("[bold]Removing epsilon rules from grammar")
    nullable_symbols = find_nullable_symbols(grammar)
    new_rules = []
    for rule in grammar.rules:
        console.print(f"[bold]Rule {cli_export.export(rule)}:")
        if len(rule.rhs) == 0:
            console.print("    Removing")
        elif nullable := [index for index, symbol in enumerate(rule.rhs) if symbol in nullable_symbols]:
            for combination in product([True, False], repeat=len(nullable)):
                new_rhs = String([
                    symbol if (index not in nullable or combination[nullable.index(index)]) else epsilon
                    for index, symbol in enumerate(rule.rhs)
                ])
                if len(new_rhs) == 0:
                    # do not add new epsilon rules
                    continue
                new_rule = ContextFreeRule(rule.lhs, String(new_rhs))
                new_rules.append(new_rule)
                console.print(f"    Creating new rule [bold]{cli_export.export(new_rule)}")
        else:
            console.print("    Rule not changed")
            new_rules.append(ContextFreeRule(rule.lhs, rule.rhs))
    return PhraseGrammar(grammar.non_terminals, grammar.terminals, new_rules, grammar.start_symbol)


def find_unit_pairs(grammar: PhraseGrammar) -> PhraseGrammar:
    """ Remove unit pairs from grammar

    Args:
        grammar: Context-free grammar

    Returns:
        Set of all unit pairs

    """
    console.rule("[bold]Finding unit pairs in grammar", style="grey")
    unit_pairs = set()
    console.print("[bold]- Step 0:")
    for symbol in grammar.non_terminals:
        unit_pairs.add((symbol, symbol))
        console.print(f"    Unit pair ({cli_export.export(symbol)}, {cli_export.export(symbol)}) added")

    changed = True
    step = 0
    while changed:
        step += 1
        changed = False
        console.print(f"[bold]- Step {step}:")
        new_pairs = set()
        for rule in grammar.rules:
            if len(rule.rhs) == 1 and rule.rhs[0] in grammar.non_terminals:
                for unit_pair in unit_pairs:
                    if unit_pair[1] == rule.lhs[0] and (unit_pair[0], rule.rhs[0]) not in unit_pairs:
                        new_pairs.add((unit_pair[0], rule.rhs[0]))
                        changed = True
                        console.print(
                            f"    Unit pair {cli_export.export(unit_pair[1])} -> {cli_export.export(rule.rhs[0])} "
                            f"added based on pair {cli_export.export(unit_pair)} and rule {cli_export.export(rule)}"
                        )
        unit_pairs = unit_pairs | new_pairs
        console.print(f"    Unit pairs: {cli_export.export(unit_pairs)}")
    console.print(f"[bold]All unit pairs found: {cli_export.export(unit_pairs)}")
    console.rule(style="gray")
    return unit_pairs


def remove_unit_rules(grammar: PhraseGrammar) -> PhraseGrammar:
    """ Remove unit rules from grammar

    Args:
        grammar: Context-free grammar

    Returns:
        New context-free grammar without unit rules

    """
    console.rule("[bold]Removing unit rules from grammar")
    unit_pairs = find_unit_pairs(grammar)
    new_rules = []
    for pair in unit_pairs:
        console.print(f"[bold]Pair {cli_export.export(pair)}:")
        for rule in grammar.rules:
            if rule.lhs[0] == pair[1] and (len(rule.rhs) != 1 or rule.rhs.is_sentence):
                new_rule = ContextFreeRule(String([pair[0]]), rule.rhs)
                new_rules.append(new_rule)
                console.print(
                    f"    Creating new rule [bold]{cli_export.export(new_rule)} "
                    f"from pair {cli_export.export(pair)} and rule {cli_export.export(rule)}"
                )
    return PhraseGrammar(grammar.non_terminals, grammar.terminals, new_rules, grammar.start_symbol)


def remove_useless_symbols(grammar: PhraseGrammar) -> PhraseGrammar:
    """ Remove useless symbols from grammar

    Args:
        grammar: Phrase grammar

    Returns:
        New phrase grammar without useless symbols

    """
    console.rule("[bold]Removing useless symbols from grammar")
    generating_symbols = find_generating_symbols(grammar)
    new_non_terminals = Alphabet({symbol for symbol in generating_symbols if symbol in grammar.non_terminals})
    new_terminals = Alphabet({symbol for symbol in generating_symbols if symbol in grammar.terminals})
    new_rules = []
    console.rule("[bold]Removing nongenerating symbols from grammar", style="grey")
    console.print(f"[bold]New non-terminal alphabet: {cli_export.export(new_non_terminals)}")
    console.print(f"[bold]New terminal alphabet: {cli_export.export(new_terminals)}")
    for rule in grammar.rules:
        if non_generating := [symbol for symbol in rule.rhs if symbol not in generating_symbols]:
            console.print(f"Removing rule {cli_export.export(rule)} as symbol {non_generating[0]} is nongenerating")
        else:
            new_rules.append(rule)

    new_grammar = PhraseGrammar(new_non_terminals, new_terminals, new_rules, grammar.start_symbol)

    reachable_symbols = find_reachable_symbols(new_grammar)
    console.rule("[bold]Removing unreachable symbols from grammar", style="grey")
    new_non_terminals = Alphabet({symbol for symbol in reachable_symbols if symbol in new_grammar.non_terminals})
    new_terminals = Alphabet({symbol for symbol in reachable_symbols if symbol in new_grammar.terminals})
    new_rules = []
    console.print(f"[bold]New non-terminal alphabet: {cli_export.export(new_non_terminals)}")
    console.print(f"[bold]New terminal alphabet: {cli_export.export(new_terminals)}")
    for rule in new_grammar.rules:
        if rule.lhs[0] not in reachable_symbols:
            console.print(f"Removing rule {cli_export.export(rule)} as symbol {rule.lhs[0]} is unreachable")
        else:
            new_rules.append(rule)

    return PhraseGrammar(grammar.non_terminals, grammar.terminals, new_rules, grammar.start_symbol)


def transform_to_chomsky(grammar: PhraseGrammar) -> PhraseGrammar:
    """ Transform grammar to Chomsky normal form

    Args:
        grammar: Phrase grammar

    Returns:
        Equivalent phrase grammar in Chomsky normal form

    """
    console.rule("[bold]Transforming grammar to Chomsky normal form", characters="#")
    console.print(Panel(cli_export.export(grammar), title="Original grammar"))

    grammar = remove_epsilon_rules(grammar)
    console.print(Panel(cli_export.export(grammar), title="Grammar without epsilon rules"))
    grammar = remove_unit_rules(grammar)
    console.print(Panel(cli_export.export(grammar), title="Grammar without unit rules"))
    grammar = remove_useless_symbols(grammar)
    console.print(Panel(cli_export.export(grammar), title="Grammar without useless symbols"))

    console.rule("Replace terminals in left-hand side")
    new_rules = []
    new_non_terminals = set()

    for rule in grammar.rules:
        if len(rule.rhs) > 1 and any(symbol in grammar.terminals for symbol in rule.rhs):
            new_rhs = []
            for symbol in rule.rhs:
                if symbol in grammar.terminals:
                    new_symbol = NonTerminal(f"Q_{symbol.id}")
                    if new_symbol not in new_non_terminals:
                        new_non_terminals.add(new_symbol)
                        terminal_rule = ContextFreeRule(String([new_symbol]), String([symbol]))
                        new_rules.append(terminal_rule)
                        console.print(
                            f"New terminal {cli_export.export(new_symbol)} "
                            f"and rule {cli_export.export(terminal_rule)} created"
                        )
                    new_rhs.append(new_symbol)
                else:
                    new_rhs.append(symbol)
            new_rule = ContextFreeRule(rule.lhs, String(new_rhs))
            console.print(f"Rule {cli_export.export(rule)} replaced with {cli_export.export(new_rule)}")
            new_rules.append(new_rule)
        else:
            new_rules.append(rule)

    grammar = PhraseGrammar(
        grammar.non_terminals.union(Alphabet(new_non_terminals)),
        grammar.terminals,
        new_rules,
        grammar.start_symbol
    )

    console.rule("Break bodies of length 3 or more")
    new_rules = []
    new_non_terminals = set()
    index = 0
    for rule in grammar.rules:
        if len(rule.rhs) > 2:
            console.print(f"[bold]Rule {cli_export.export(rule)} replaced with rules:")
            last_symbol = rule.lhs[0]
            for symbol in rule.rhs[:-2]:
                new_symbol = NonTerminal(f"K_{index}")
                index += 1
                new_non_terminals.add(new_symbol)
                new_rule = ContextFreeRule(String([last_symbol]), String([symbol, new_symbol]))
                console.print(f"    {cli_export.export(new_rule)}")
                new_rules.append(new_rule)
                last_symbol = new_symbol
            new_rule = ContextFreeRule(String([last_symbol]), String(rule.rhs[-2:]))
            console.print(f"    {cli_export.export(new_rule)}")
            new_rules.append(new_rule)
        else:
            new_rules.append(rule)

    final_grammar = PhraseGrammar(
        grammar.non_terminals.union(Alphabet(new_non_terminals)),
        grammar.terminals,
        new_rules,
        grammar.start_symbol
    )
    console.print(Panel(cli_export.export(final_grammar), title="Final grammar"))

    return final_grammar
