class Tree:
    def __init__(self):
        self.roots = []
        self.len = 0
        self.frontier = []

    def add_root(self, node):
        self.len = 1
        self.roots.append(node)
        self.frontier = [node]

    def create_node(self, *args, **kwargs):
        new_node = TreeNode(self, self.len, *args, **kwargs)
        self.len += 1
        return new_node

    def print(self):
        for root in self.roots:
            root.print(0)

    def merge(self, other):
        self.roots = self.roots + other.roots
        self.len = self.len + other.len
        self.frontier = self.frontier + other.frontier
        return self


class TreeNode:
    def __init__(self, tree, index, data, depth):
        self.tree = tree
        self.data = data
        self.depth = depth
        self.index = index
        self.children = []
        self.is_frontier = True
        self.parents = []

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
            child.parents.append(self)

    def add_parent(self, parent):
        self.parents.append(parent)

    def remove_from_frontier(self):
        if not self.is_frontier:
            return
        for i, node in enumerate(self.tree.frontier):
            if node is self:
                self.tree.frontier = self.tree.frontier[:i] + self.tree.frontier[i+1:]
                break
        self.is_frontier = False


    def print(self, indent):
        print("  " * indent + str(self.data))
        for child in self.children:
            child.print(indent+1)
