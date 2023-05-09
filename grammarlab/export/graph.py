from functools import reduce

from grammarlab.core.ast import Tree
from grammarlab.core.visualize_ast import visualize_ast
from grammarlab.export.export import Export, formatter
from grammarlab.grammars.pc_grammar_system import CommunicationRule, PCConfiguration
from grammarlab.grammars.phrase_grammar import PhraseConfiguration
from grammarlab.grammars.scattered_context_grammar import SCGConfiguration


class GraphExport(Export):
    @formatter(PhraseConfiguration)
    def phrase_configuration(self, configuration: PhraseConfiguration, depth: int = 0, tree=None, filename=None):
        if not tree and not configuration.parent:
            tree = Tree()
            root_node = tree.create_node(configuration.data[0], depth=depth)
            tree.add_root(root_node)
        else:
            # recursively create AST from parent
            tree = tree or self.export(configuration.parent, depth=depth+1)

            # apply rule to parent AST
            parents = tree.frontier[configuration.affected:configuration.affected + len(configuration.used_rule.lhs)]
            children = [tree.create_node(x, depth) for x in configuration.used_rule.rhs]
            parents[0].add_children(children)
            for parent in parents[1:]:
                parent.remove_from_frontier()
                for child in children:
                    child.add_parent(parent)

        if filename:
            visualize_ast(tree, filename)

        return tree

    @formatter(SCGConfiguration)
    def scg_configuration(self, configuration: PhraseConfiguration, depth: int = 0, tree=None, filename=None):
        if not tree and not configuration.parent:
            tree = Tree()
            root_node = tree.create_node(configuration.data[0], depth=depth)
            tree.add_root(root_node)
        else:
            # recursively create AST from parent
            tree = tree or self.export(configuration.parent, depth=depth + 1)

            # apply rule to parent AST
            lhs_nodes = []
            for position in configuration.affected:
                lhs_nodes.append(tree.frontier[position])

            for i, string in enumerate(configuration.used_rule.rhs):
                children = [tree.create_node(x, depth) for x in string]
                lhs_nodes[i].add_children(children)

        if filename:
            visualize_ast(tree, filename)

        return tree

    @formatter(PCConfiguration)
    def pc_configuration(self, configuration: PhraseConfiguration, depth: int = 0, filename=None):
        if not configuration.parent:
            trees = [
                self.export(c, depth=depth) for c in configuration.data
            ]
        else:
            # recursively create AST from parent
            trees = self.export(configuration.parent, depth=depth + 1)

            # apply rule to parent AST
            for i, tree in enumerate(trees):
                component = configuration[i]
                if isinstance(configuration.used_rule, CommunicationRule):
                    if component.used_rule == "return":
                        new_node = tree.create_node(component.data[0], depth)
                        tree.frontier[0].add_children([new_node])
                        for parent in tree.frontier[1:]:
                            new_node.add_parent(parent)
                            parent.remove_from_frontier()
                    elif component.used_rule == "communication":
                        parents = [tree.frontier[x] for x in component.affected]
                        for parent in parents:
                            symbol = parent.data
                            rhs = configuration.used_rule[symbol]
                            children = [tree.create_node(x, depth) for x in rhs]
                            parent.add_children(children)
                else:
                    self.export(component, depth, tree=tree)

        if filename:
            tree = reduce(lambda a, b: a.merge(b), trees)
            visualize_ast(tree, filename)

        return trees
