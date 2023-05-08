"""Examples of GrammarLab usage. These folder contains grammar for selected languages.

You can run them from the command line:

.. code-block:: console

    $ python pc_power_of_two.py generate
    a a
    a a a a
    a a a a a a a a
    ...

    $ python cf_dyck.py derivation_sequence -s "aaaaaaaa"
    | Used Rule   | Sential Form   |
    |-------------+----------------|
    |             | S              |
    | S -> ( S )  | ( S )          |
    | S -> S S    | ( S S )        |
    | S -> ( )    | ( ( ) S )      |
    | S -> ( )    | ( ( ) ( ) )    |


Full documentation of command line interface can be found in :class:`glab.core.app.App` section.

If you want to use grammar in your code, you can use :class:`glab.core.grammar_base.GrammarBase` class directly:

.. code-block:: python

    >>> from glab.examples.pc_power_of_two import grammar
    >>> result = grammar.derive(depth=3)
    >>> result = [str(x.sential_form) for x in result]
    >>> print(result)
    ['a a']

"""