

class Node:
    def __init__(self, level=None, data=None, size=27):
        self.link = [None]*size  # where $ is at index 0
        self.data = data         # data payload
        self.level = level


class Trie:
    def __init__(self):
        self.root = Node(level=0)  # root does not save anything
        self.total_words = 0  # number of unique words stored

    def insert(self, key, data=None):
        # begin from the root
        current = self.root
        # go through the key 1 by 1
        count_level = 0
        for i in range(len(key) + 1):
            count_level += 1
            if i == len(key):
                # go through terminal at the end
                index = 0
            else:
                # $ = 0, a = 1, b = 2 ......
                index = ord(key[i]) - 97 + 1

            # node exists, traverse
            if current.link[index] is None:
                current.link[index] = Node(level=count_level)
                # if new word is inserted (new node created for '$' at the end)
                if index == 0:
                    self.total_words += 1
            current = current.link[index]

        # add in payload at the leaf
        # at the end of the for loop, you're at the leaf
        current.data = data

    def insert_recurse(self, key, data=None):
        current = self.root
        self.insert_recurse_aux(key, data, current)

    def insert_recurse_aux(self, key, data, current, char=0):
        if char == len(key):  # if reach end of key, where terminal should be
            if current.link[0] is None:
                current.link[0] = Node(level=char+1)
                self.total_words += 1  # if new word is inserted
            current.link[0].data = data
            return
        else:
            next_ind = ord(key[char]) - 97 + 1
            # if no node, create node, otherwise just traverse
            if current.link[next_ind] is None:
                current.link[next_ind] = Node(level=char+1)
            self.insert_recurse_aux(key, data, current.link[next_ind], char + 1)

    def search(self, key):
        # begin from the root
        current = self.root
        # go through the key 1 by 1
        for i in range(len(key) + 1):
            if i == len(key):  # go through terminal at the end
                index = 0
            else:
                # $ = 0, a = 1, b = 2 ......
                index = ord(key[i]) - 97 + 1

            # node exists
            if current.link[index] is not None:
                current = current.link[index]
                if index == 0:
                    return current.data
            # node does not exist
            else:
                raise Exception(str(key) + " does not exist. ")

    def search_recurse(self, key):
        current = self.root
        return self.search_recurse_aux(key, current)

    def search_recurse_aux(self, key, current, char=0):
        # if reach the end of the key, now looking at terminal character
        if char == len(key):
            if current.link[0] is None:
                raise Exception(str(key) + " does not exist")
            else:
                return current.link[0].data
        else:
            next_ind = ord(key[char]) - 97 + 1
            # if no node, raise exception, otherwise just traverse
            if current.link[next_ind] is None:
                raise Exception(str(key) + " does not exist")
            return self.search_recurse_aux(key, current.link[next_ind], char + 1)

    def build_suffix_trie(self, key):
        """ Given a string, key, builds a suffix trie for it

        :complexity: O(K^2), where K is the length of the key
        """
        for char in range(len(key)):
            current = self.root
            for c in range(char, len(key) + 1):
                index = 0 if c == len(key) else ord(key[c]) - 97 + 1
                # if node does not exist, create node then traverse
                # otherwise just traverse
                if current.link[index] is None:
                    current.link[index] = Node(level=c)
                    # if new word is inserted
                    if index == 0:
                        self.total_words += 1
                current = current.link[index]
            current.data = char + 1  # suffix id

    def traverse_preorder(self, current=None, data_array=None):
        """ Retrieve data from the leaves in pre-order sequence
        :time complexity: O(N), where N is the number of nodes in the trie
        """
        if current is None:
            current = self.root
            data_array = [0]
            return self.traverse_preorder(current, data_array)
        else:
            # visit root first, then from left to right
            if current.data is not None:
                data_array.append(current.data)

            for i in range(len(current.link)):
                if current.link[i] is not None:
                    self.traverse_preorder(current.link[i], data_array)
            return data_array


