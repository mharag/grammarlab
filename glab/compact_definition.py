""" This module simplifies definition of strings, rules and grammars

Instead of verbose definitions like String([Symbol("A"), Symbol("B")])
compact definitions ("AB") from this module can be used.

"""

from typing import Iterable, List, Optional

from glab.alphabet import Alphabet, NonTerminal, String, Terminal


def compact_nonterminal_alphabet(raw_alphabet: Iterable) -> Alphabet:
    """Get nonterminal alphabet from characters

    Args:
        raw_alphabet: any iterable object.
    Returns:
        Alphabet of nonterminals with elements from raw_alphabet

    """
    symbols = {NonTerminal(symbol) for symbol in raw_alphabet}
    return Alphabet(symbols)


def compact_terminal_alphabet(raw_alphabet: Iterable) -> Alphabet:
    """Get terminal alphabet from characters

    Args:
        raw_alphabet: any iterable object.
    Returns:
        Alphabet of terminals with elements from raw_alphabet

    """
    symbols = {Terminal(symbol) for symbol in raw_alphabet}
    return Alphabet(symbols)


def compact_communication_symbols(raw_symbols: List) -> List[NonTerminal]:
    """Return list of communication symbols

    Args:
        raw_symbols: lit of symbol representations

    Returns:
        list of symbols
    """
    symbols = [NonTerminal(symbol) for symbol in raw_symbols]
    return symbols


def compact_string(alphabet: Alphabet, string: str, delimiter: Optional[str] = None):
    """ Create string compact representation

    Compact definition of string can be for example:
    "abcd", "a,b_n,c,d"

    Args:
        alphabet: alphabet of all symbols in string
        string: representation of string
        delimiter: str that separate symbols in string

    Returns:
        String

    """
    result = []
    if delimiter:
        string = string.split(delimiter)
    for symbol in string:
        result.append(alphabet.lookup(symbol))
    return String(result)
