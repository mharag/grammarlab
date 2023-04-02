import graphviz


def visualize_ast(ast):
    u = graphviz.Digraph('unix', filename='unix.gv')

    queue = [ast.root]
    lines = {}
    while queue:
        node = queue.pop(0)
        if node.depth not in lines:
            lines[node.depth] = graphviz.Digraph(str(node.depth))
            lines[node.depth].attr(rank="same")
        line = lines[node.depth]
        line.node(f"{node.index}|{node.data}", str(node.data))
        for child in node.children:
            queue.append(child)

    for line in lines.values():
        u.subgraph(line)

    queue = [ast.root]
    while queue:
        node = queue.pop(0)
        if node.parent:
            u.edge(f"{node.parent.index}|{node.parent.data}", f"{node.index}|{node.data}")
        for child in node.children:
            queue.append(child)

    u.view()
