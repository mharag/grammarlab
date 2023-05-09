"""This directory contains all _exporters.

Exporters are used to export some object to certain format.
One export is responsible for one format.
For example, :class:`glab.export.cli.CliExport` exports object to command line
and :class:`glab.export.code.CodeExport` exports object to python code.
Details about exporter behavior can be found in :mod:`glab.export.export` module.

If you want to extend glab with new exporter, you can do it by creating new
class that inherits from :class:`glab.export.export.Export` and add
decorator :func:`glab.export.export.formatter` to each method that should
export some object. Please note convention that method name should be the same
as class name of exported object. Method names are not relevant in this case, but
it helps to keep code readable.

Every formatter contains example of it's output it docstring.

"""

from glab.export.cli import CliExport
from glab.export.code import CodeExport
from glab.export.graph import GraphExport
from glab.export.latex import LatexExport
