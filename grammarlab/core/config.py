"""Global configuration for GrammarLab.

"""

from enum import Enum

STRING_DELIMITER = " "
"""Delimiter used to join symbols in a string.

If you have only one character symbol you can set this to an empty string.

"""
COLOR_CLI_OUTPUT = True
"""If set to True, the CLI output will be colored."""


class Color(Enum):
    """Possible colors for CLI output.

    """
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
