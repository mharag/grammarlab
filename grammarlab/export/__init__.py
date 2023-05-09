"""This directory contains all _exporters.

Exporters are used to export some object to certain format.
One export is responsible for one format.
For example, :class:`grammarlab.export.cli.CliExport` exports object to command line
and :class:`grammarlab.export.code.CodeExport` exports object to python code.
Details about exporter behavior can be found in :mod:`grammarlab.export.export` module.

If you want to extend grammarlab with new exporter, you can do it by creating new
class that inherits from :class:`grammarlab.export.export.Export` and add
decorator :func:`grammarlab.export.export.formatter` to each method that should
export some object. Please note convention that method name should be the same
as class name of exported object. Method names are not relevant in this case, but
it helps to keep code readable.

Every formatter contains example of it's output it docstring.

"""

from grammarlab.export.cli import CliExport
from grammarlab.export.code import CodeExport
from grammarlab.export.graph import GraphExport
from grammarlab.export.latex import LatexExport
