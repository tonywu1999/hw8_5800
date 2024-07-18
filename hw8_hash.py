import numpy as np
import matplotlib.pyplot as plt
class Node:
    key = None
    next_node = None
    value = None

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:

    def __init__(self, m: int):
        self.table = [None] * m
        self.m = m

    def hash_function(self, key: str) -> int:
        sum_ascii = 0
        for i in range(len(key)):
            ascii_value = ord(key[i])
            sum_ascii += (ascii_value**2) * (i**2)
        return sum_ascii % self.m

    def insert(self, key, value):
        index = self.hash_function(key)
        node = self.table[index]
        if node is None:
            self.table[index] = Node(key, value)
        else:
            match = False
            while node is not None:
                if node.key == key:
                    node.value += value
                    match = True
                    break
                else:
                    node = node.next_node
            if not match:
                node = Node(key, value)
                node.next_node = self.table[index]
                self.table[index] = node

    def delete(self, key):
        index = self.hash_function(key)
        node = self.table[index]
        if node is None:
            return
        elif node.key == key:
            self.table[index] = node.next_node
        else:
            prev_node = node
            node = node.next_node
            while node is not None:
                if node.key == key:
                    prev_node.next_node = node.next_node
                    break
                else:
                    prev_node = node
                    node = node.next_node

    def increase(self, key):
        index = self.hash_function(key)
        node = self.table[index]
        while node is not None:
            if node.key == key:
                node.value += 1
                break
            else:
                node = node.next_node

    def find(self, key):
        index = self.hash_function(key)
        node = self.table[index]
        if node is None:
            return None
        else:
            match = False
            while node is not None:
                if node.key == key:
                    return node
                else:
                    node = node.next_node
            if not match:
                return None

    def list_all_keys(self):
        key_list = []
        for i in range(self.m):
            node = self.table[i]
            while node is not None:
                key_list.append(node.key)
                node = node.next_node
        return key_list

    def generate_distribution(self):
        distribution_list = []
        counts_list = []
        for i in range(self.m):
            node = self.table[i]
            count = 0
            while node is not None:
                count += 1
                distribution_list.append(i)
                node = node.next_node
            counts_list.append(count)
        return distribution_list, counts_list



if __name__ == "__main__":
    text_file = open("wonderland.txt", "r")
    words = text_file.read().split()
    text_file.close()
    hashtable_30 = HashTable(30)
    hashtable_300 = HashTable(300)
    hashtable_1000 = HashTable(1000)
    for word in words:
        hashtable_30.insert(word, 1)
        hashtable_300.insert(word, 1)
        hashtable_1000.insert(word, 1)
    print(hashtable_30.list_all_keys())
    print(hashtable_30.find("teacup").value)
    hashtable_30.increase("teacup")
    print(hashtable_30.find("teacup").value)
    hashtable_30.delete("teacup")
    print(hashtable_30.find("teacup"))
    hashtable_30.insert("apple", 1)
    hashtable_30.insert("banana", 1)
    hashtable_300.insert("apple", 1)
    hashtable_300.insert("banana", 1)
    hashtable_1000.insert("apple", 1)
    hashtable_1000.insert("banana", 1)
    print(hashtable_30.find("apple").key)
    print(hashtable_30.find("apple").value)
    print(hashtable_30.find("banana").key)
    print(hashtable_30.find("banana").value)
    print(hashtable_30.find("grape"))
    # generate histogram with matplotlib of hashtable collisions and calculate variance.
    distribution_list, counts_list = hashtable_1000.generate_distribution()
    print(np.var(counts_list))
    plt.hist(distribution_list)
    plt.show()


