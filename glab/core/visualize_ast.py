import graphviz


def visualize_ast(ast, filename):
    filename = filename or "ast"
    graph = graphviz.Digraph('AST', filename=filename)

    # ast can have multiple roots (for example PC grammar system)
    for i, root in enumerate(ast.roots):
        queue = [root]
        # every line in the graph is a separate graph to ensure that nodes are on the same level
        lines = {}
        # process all nodes in BFS order
        while queue:
            node = queue.pop(0)
            if node.depth not in lines:
                lines[node.depth] = graphviz.Digraph(str(node.depth))
                lines[node.depth].attr(rank="same")
            line = lines[node.depth]
            # one symbol can be used multiple times in the same graph - add index to distinguish them
            line.node(f"{i}|{node.index}|{node.data}", str(node.data))
            for child in node.children:
                queue.append(child)

        # add all lines to the graph
        for line in lines.values():
            graph.subgraph(line)

        # add edges
        queue = [root]
        while queue:
            node = queue.pop(0)
            for parent in node.parents:
                graph.edge(f"{i}|{parent.index}|{parent.data}", f"{i}|{node.index}|{node.data}")
            for child in node.children:
                queue.append(child)

    # open graph
    print("Abstract syntax tree visualization saved to file ./{filename}.pdf")
    graph.view()
