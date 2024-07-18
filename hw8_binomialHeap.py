import math
import random
class Node:
    key = None
    child = None
    parent = None
    sibling = None
    degree = None

    def __init__(self, key):
        self.key = key


class BinomialHeap:

    def __init__(self, key):
        node = Node(key)
        node.degree = 0
        self.head = node
        self.min = node

    def insert(self, key):
        new_node = Node(key)
        if self.minimum().key > key:
            self.min = new_node
        new_node.degree = 0
        root_node = self.head
        if root_node.degree == new_node.degree:
            while root_node.degree == new_node.degree:
                if root_node.key > new_node.key:
                    if self.head == root_node:
                        self.head = new_node
                    new_node.sibling = root_node.sibling
                    self.union(new_node, root_node)
                    root_node = new_node.sibling
                else:
                    if self.head == new_node:
                        self.head = root_node
                    self.union(root_node, new_node)
                    new_node = root_node
                    root_node = root_node.sibling
                if root_node is None:
                    return
        else:
            new_node.sibling = root_node
            self.head = new_node

    def minimum(self):
        return self.min

    def extract_min(self):
        """When considering amortized-like analysis, this is O(log n)"""
        node = self.head
        root_stack = []
        while node != self.minimum():
            root_stack.append(node)
            if node.sibling == self.minimum():
                node.sibling = self.minimum().sibling
            node = node.sibling
        node = self.minimum().child
        child_queue = []
        while node is not None:
            child_queue.append(node)
            node.parent = None
            node = node.sibling

        if len(root_stack) > 0 and len(child_queue) > 0:
            root_node = root_stack.pop()
            child_node = child_queue.pop(0)
            while root_node is not None:
                if root_node.degree == child_node.degree:
                    while root_node.degree == child_node.degree:
                        if root_node.key > child_node.key:
                            if self.head == root_node:
                                self.head = child_node
                            child_node.sibling = root_node.sibling
                            self.union(child_node, root_node)
                            root_node = child_node.sibling
                        else:
                            if self.head == child_node:
                                self.head = child_node
                            self.union(root_node, child_node)
                            child_node = root_node
                            root_node = root_node.sibling
                        if root_node is None:
                            break
                    if len(child_queue) > 0 and len(root_stack) > 0:
                        child_node = child_queue.pop(0)
                        root_node = root_stack.pop()
                    else:
                        break
                else:
                    if root_node.degree < child_node.degree:
                        child_node.sibling = root_node.sibling
                        root_node.sibling = child_node
                        if len(child_queue) == 0:
                            break
                        else:
                            child_node = child_queue.pop(0)
                    else:
                        if len(root_stack) == 0:
                            break
                        else:
                            root_node = root_stack.pop()

        if len(child_queue) > 0:
            old_head = self.head
            self.head = child_queue.pop()
            node = self.head
            while len(child_queue) > 0:
                node.sibling = child_queue.pop()
                node = node.sibling
            if old_head != self.minimum():
                node.sibling = old_head
            else:
                node.sibling = self.minimum().sibling

        node = self.head
        self.min = node
        while node is not None:
            if node.key < self.minimum().key:
                self.min = node
            node = node.sibling

    def union(self, node_1, node_2):
        node_2.sibling = node_1.child
        node_2.parent = node_1
        node_1.child = node_2
        node_1.degree += 1
        return node_1

    def decrease_key(self, key, new_value):
        node = self.search(key)
        node.key = new_value
        while node.parent is not None:
            if node.key < node.parent.key:
                dummy_value = node.key
                node.key = node.parent.key
                node.parent.key = dummy_value
                node = node.parent
        if new_value < self.minimum().key:
            self.min = node
        return node

    def delete(self, key):
        self.decrease_key(key, -math.inf)
        self.extract_min()

    def search(self, key):
        node = self.head
        while node is not None:
            if node.key == key:
                return node
            result = self.search_node(node.child, key)
            if result is not None:
                return result
            node = node.sibling
        raise Exception("Node not found")

    def search_node(self, node, key):
        if node is None:
            return None
        if node.key == key:
            return node
        elif key > node.key:
            option_1 = self.search_node(node.child, key)
            option_2 = self.search_node(node.sibling, key)
            return option_1 if option_2 is None else option_2
        else:
            return self.search_node(node.sibling, key)


if __name__ == "__main__":
    binomial_heap = BinomialHeap(5)
    values = [3, 2, 6, 1, 10, 9, 4]
    for value in values:
        binomial_heap.insert(value)
    print(binomial_heap.search(6).key)
    binomial_heap.delete(6)
    binomial_heap.search(6)





