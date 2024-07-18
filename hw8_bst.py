class Node:
    key = None
    left_child = None
    right_child = None
    color = None
    parent = None

    def __init__(self, key):
        self.key = key


class RBTree:

    def __init__(self, key):
        node = Node(key)
        node.color = "K"
        self.root = node

    def search(self, key):
        node = self.root
        while node is not None:
            if key > node.key:
                node = node.right_child
            elif key < node.key:
                node = node.left_child
            else:
                return node
        raise Exception("Key not found")

    def min_node(self, node):
        while node.left_child is not None:
            node = node.left_child
        return node

    def inorder_traversal(self):
        node = self.root
        node = self.min_node(self.root)
        while node is not None:
            print(node.key)
            node = self.successor(node.key)


    def max_node(self, node):
        while node.right_child is not None:
            node = node.right_child
        return node

    def min(self):
        return self.min_node(self.root).key

    def max(self):
        return self.max_node(self.root).key

    def successor(self, key):
        node = self.search(key)
        if node.right_child is not None:
            return self.min_node(node.right_child)
        else:
            ancestor = node.parent
            while ancestor is not None and node == ancestor.right_child:
                node = ancestor
                ancestor = ancestor.parent
            return ancestor

    def predecessor(self, key):
        node = self.search(key)
        if node.left_child is not None:
            return self.max_node(node.left_child)
        else:
            ancestor = node.parent
            while ancestor is not None and node == ancestor.left_child:
                node = ancestor
                ancestor = ancestor.parent
            return ancestor

    def rotation(self, node, direction):
        if direction == "right":
            # alpha <= X (left child) <= beta <= node <= gamma
            x = node.left_child
            if node == self.root:
                self.root = x
            beta = x.right_child
            x.right_child = node
            x.parent = node.parent
            if x.parent is not None:
                if x.parent.right_child == node:
                    x.parent.right_child = x
                else:
                    x.parent.left_child = x
            node.parent = x
            node.left_child = beta
            if beta is not None:
                beta.parent = node
        elif direction == "left":
            # alpha <= node <= beta <= y (right child) <= gamma
            y = node.right_child
            if node == self.root:
                self.root = y
            beta = y.left_child
            y.left_child = node
            y.parent = node.parent
            if y.parent is not None:
                if y.parent.right_child == node:
                    y.parent.right_child = y
                else:
                    y.parent.left_child = y
            node.parent = y
            node.right_child = beta
            if beta is not None:
                beta.parent = node
        else:
            raise Exception("Give proper rotation direction")

    def insert(self, key):
        parent = self.root
        new_node = None
        while parent is not None:
            if key > parent.key:
                if parent.right_child is None:
                    new_node = Node(key)
                    parent.right_child = new_node
                    new_node.parent = parent
                    new_node.color = "R"
                    break
                else:
                    parent = parent.right_child
            else:
                if parent.left_child is None:
                    new_node = Node(key)
                    parent.left_child = new_node
                    new_node.parent = parent
                    new_node.color = "R"
                    break
                else:
                    parent = parent.left_child
        self.insert_fixup(new_node)

    def insert_fixup(self, node):
        while node.parent is not None and node.parent.color == "R":
            if node.parent == node.parent.parent.left_child:
                uncle = node.parent.parent.right_child
                if uncle is not None and uncle.color == "R":
                    # Case 1
                    node.parent.parent.color = "R"
                    uncle.color = "K"
                    node.parent.color = "K"
                    node = node.parent.parent
                else:
                    # Case 2
                    if node.parent.right_child == node:
                        node = node.parent
                        self.rotation(node, "left")
                    # Case 3
                    node.parent.color = "K"
                    node.parent.parent.color = "R"
                    self.rotation(node.parent.parent, "right")
            else:
                uncle = node.parent.parent.left_child
                if uncle is not None and uncle.color == "R":
                    # Case 1
                    node.parent.parent.color = "R"
                    uncle.color = "K"
                    node.parent.color = "K"
                    node = node.parent.parent
                else:
                    # Case 2
                    if node.parent.left_child == node:
                        node = node.parent
                        self.rotation(node, "right")
                    # Case 3
                    node.parent.color = "K"
                    node.parent.parent.color = "R"
                    self.rotation(node.parent.parent, "left")
        self.root.color = "K"

    def delete(self, key):
        node = self.search(key)
        if node.left_child is None and node.right_child is None:
            parent = node.parent
            if parent.right_child == node:
                parent.right_child = None
            else:
                parent.left_child = None
        elif node.left_child is None or node.right_child is None:
            parent = node.parent
            if parent.right_child == node:
                parent.right_child = node.right_child if node.right_child is not None else node.left_child
                parent.right_child.parent = parent
            else:
                parent.left_child = node.right_child if node.right_child is not None else node.left_child
                parent.left_child.parent = parent
        else:
            parent = node.parent
            right_child = node.right_child
            if right_child.left_child is None:
                # Case 1: Right child takes Z's spot
                right_child.left_child = node.left_child
                right_child.parent = node.parent
                right_child.left_child.parent = right_child
                if parent is not None:
                    if parent.right_child == node:
                        parent.right_child = right_child
                    else:
                        parent.left_child = right_child
                else:
                    self.root = right_child
            else:
                # Case 2: Successor takes Z's spot
                successor = self.successor(node.key)
                successor.parent.left_child = None
                successor.parent = node.parent
                successor.left_child = node.left_child
                successor.right_child = node.right_child
                successor.left_child.parent = successor
                successor.right_child.parent = successor
                if parent is not None:
                    if parent.right_child == node:
                        parent.right_child = successor
                    else:
                        parent.left_child = successor
                else:
                    self.root = successor

    def print_tree(self):
        node = self.root
        self.print_tree_rec(node, 0)

    def print_tree_rec(self, node, level):
        if node is not None:
            self.print_tree_rec(node.right_child, level + 1)
            print(' ' * 4 * level + '-> ' + str(node.key) + ': ' + str(node.color))
            self.print_tree_rec(node.left_child, level + 1)



if __name__ == "__main__":
    numbers = [14, 2, 1, 7, 15, 5, 8, 4]
    tree = RBTree(11)
    for number in numbers:
        tree.insert(number)
    while True:
        tree.insert(10)
        tree.print_tree()
        tree.insert(9)
        tree.insert(6)
        tree.insert(3)
        tree.delete(7)
        tree.print_tree()
