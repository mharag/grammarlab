# GrammarLab

## Description
GrammarLab is a python library for creating, testing and playing with various types of grammars.

## What can you do with GrammarLab?
With GrammarLab you can:
* Easily define a grammar
* Generate language of a grammar
* Check if a word belongs to the language of grammar
* Generate derivation sequence for a word
* Generate abstract syntax tree for a word
* Export grammar to LaTeX, python code or plain text
* Check if grammar is in regular form
* Convert grammar to regular form
* ...

## Supported grammar types
* Phrase grammars (contex-free, context-sensitive, unrestricted)
* Scattered Context Grammars
* Parallel Communicating Grammar Systems
* More comming...

## Installation
Do not forget to add file `grammarlab` to your `PYTHONPATH` environment variable.
```bash
export PYTHONPATH=$(PWD):$PYTHONPATH
```
Official release are comming soon. Keep an eye on this repository :)

## Documentation
Full documentation id available at ``docs/_build/html/index.html``
You can also build the documentation yourself by running:
```bash
cd docs
make html
```


## Getting started
You can check one of the examples in the examples folder to see how to use GrammarLab.
```bash
python3 grammarlab/examples/pc_power_of_two.py ast -s "a a a a a a a a" -d " "
python3 grammarlab/examples/cf_dyck.py derivation_sequence -s "()()()()(())"
python3 grammarlab/examples/cs_aaa.py generate -d 100
```
You can also try out the transformation to Chomsky normal form.
Create a file named `script.py` with the following content:
```python
from grammarlab.transformations.chomsky_normal_form import transform_to_chomsky
from grammarlab.examples.cf_dyck import grammar
from grammarlab.core.app import App


new_grammar = transform_to_chomsky(grammar)

if __name__ == "__main__":
    App(new_grammar).run()
```
And then run the script:
```bash
python3 script.py
python3 script.py export --code
python3 generate -d 20
```

## Testing
You can run the tests by running:
```bash
pytest
```
in the root directory of the project.

## License
This package is licensed under the MIT License. See the LICENSE file for more information.
