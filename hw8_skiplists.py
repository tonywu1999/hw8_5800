import math
import random
class Node:
    key = None
    next_node = None
    prev_node = None
    up_node = None
    down_node = None

    def __init__(self, key):
        self.key = key


class SkipList:

    def __init__(self):
        node_negative_inf = Node(-math.inf)
        node_inf = Node(math.inf)
        node_negative_inf.next_node = node_inf
        node_inf.prev_node = node_negative_inf
        self.levels = [node_negative_inf]

    def insert(self, key):
        level = len(self.levels) - 1
        node = self.levels[level]
        next_node = node.next_node
        while True:
            if node.key < key < next_node.key:
                if level == 0:
                    new_node = Node(key)
                    node.next_node = new_node
                    next_node.prev_node = new_node
                    new_node.next_node = next_node
                    new_node.prev_node = node
                    while True:
                        random_number = random.randint(0,1)
                        if random_number:
                            if level == len(self.levels) - 1:
                                # create new level
                                node_negative_inf = Node(-math.inf)
                                newer_node = Node(key)
                                node_inf = Node(math.inf)

                                node_negative_inf.next_node = newer_node
                                newer_node.next_node = node_inf
                                newer_node.prev_node = node_negative_inf
                                node_inf.prev_node = newer_node

                                new_node.up_node = newer_node
                                self.levels[level].up_node = node_negative_inf
                                newer_node.down_node = new_node
                                node_negative_inf.down_node = self.levels[level]

                                self.levels.append(node_negative_inf)
                                new_node = newer_node
                            else:
                                # Find next level node
                                traversing_node = new_node.prev_node
                                while traversing_node.up_node is None:
                                    traversing_node = traversing_node.prev_node
                                traversing_node = traversing_node.up_node
                                next_traversing_node = traversing_node.next_node
                                newer_node = Node(key)

                                traversing_node.next_node = newer_node
                                newer_node.next_node = next_traversing_node
                                newer_node.prev_node = traversing_node
                                next_traversing_node.prev_node = newer_node

                                new_node.up_node = newer_node
                                newer_node.down_node = new_node
                                new_node = newer_node
                            level += 1
                        else:
                            return key
                else:
                    node = node.down_node
                    next_node = node.next_node
                    level = level - 1
            elif node.key == key:
                raise Exception("key is already present")
            else:
                node = node.next_node
                next_node = next_node.next_node

    def delete(self, key):
        node = self.lookup_node(key)
        while True:
            prev_node = node.prev_node
            next_node = node.next_node
            prev_node.next_node = next_node
            next_node.prev_node = prev_node
            if node.down_node is None:
                break
            else:
                node = node.down_node

    def lookup_node(self, key):
        level = len(self.levels) - 1
        node = self.levels[level]
        next_node = node.next_node
        while True:
            if node.key < key < next_node.key:
                if level == 0:
                    raise Exception("Key not found")
                else:
                    print(f'Level {level}: comparison {key} vs {node.key} and {next_node.key} - move down')
                    node = node.down_node
                    next_node = node.next_node
                    level = level - 1
            elif node.key == key:
                return node
            else:
                print(f'Level {level}: comparison {key} vs {node.key} and {next_node.key} - move right')
                node = node.next_node
                next_node = next_node.next_node

    def lookup(self, key):
        return self.lookup_node(key).key

    def print_skip_list(self):
        level = len(self.levels) - 1
        while level >= 0:
            node = self.levels[level]
            print_string = ''
            while node is not None:
                print_string = f'{print_string} {node.key} -> '
                node = node.next_node
            print(print_string)
            level = level - 1


if __name__ == "__main__":
    skipList = SkipList()
    values = [5, 3, 2, 6, 1, 10, 9, 4]
    for value in values:
        skipList.insert(value)

    skipList.print_skip_list()
    print(skipList.lookup(5))
    print(skipList.lookup(3))
    print(skipList.lookup(2))
    print(skipList.lookup(4))
    print(skipList.lookup(6))
    print(skipList.lookup(1))
    print(skipList.lookup(10))
    print(skipList.lookup(9))
    skipList.delete(9)
    skipList.print_skip_list()
    print(skipList.lookup(5))
    print(skipList.lookup(3))
    print(skipList.lookup(2))
    print(skipList.lookup(4))
    print(skipList.lookup(6))
    print(skipList.lookup(1))
    print(skipList.lookup(10))
    skipList.insert(9)
    skipList.print_skip_list()
    print(skipList.lookup(9))




