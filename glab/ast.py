class Tree:
    def __init__(self):
        self.root = None
        self.len = 0
        self.frontier = []

    def add_root(self, node):
        self.len = 1
        self.root = node
        self.frontier = [node]

    def create_node(self, *args, **kwargs):
        new_node = TreeNode(self, self.len, *args, **kwargs)
        self.len += 1
        return new_node

    def print(self):
        self.root.print(0)


class TreeNode:
    def __init__(self, tree, index, data, depth):
        self.tree = tree
        self.data = data
        self.depth = depth
        self.index = index
        self.children = []
        self.is_frontier = True
        self.parent = None

    def add_children(self, children):
        if not self.is_frontier:
            raise ValueError("Trying to add children to node that is not in frontier!")
        self.children = children
        self.is_frontier = False
        for i, node in enumerate(self.tree.frontier):
            if node is self:
                self.tree.frontier[i:i+1] = children
                break
        else:
            raise ValueError("Node not in frontier even though it should be there!")
        for child in children:
            child.parent = self

    def print(self, indent):
        print("  " * indent + str(self.data))
        for child in self.children:
            child.print(indent+1)


