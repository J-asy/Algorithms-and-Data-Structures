"""

This file contains the following classes:
1) Node, which represents a node in the prefix / suffix trie with relevant information
2) Trie, which has the following functions:
__init__, insert_prefix, insert_prefix_aux, build_suffix_trie, search_longest_suffix and sum_lexicographically_less

More notably, this file contains the functions for the applications of tries:
1) build_from_substrings(S, T)
2) alpha_pos(text, query_list)
"""


class Node:
    """ Represents a node in a prefix / suffix trie with the instance variables:
    self.link: an array that will store the memory locations of the node's children
    self.frequency: the number of words that particular node is a part of
    self.id: the suffix id of a suffix (for suffix tries)
    self.level: the index of a character represented by the node in the given key (for suffix tries)
    """
    def __init__(self, frequency=1, suffix_id=None, lvl=None, size=27):
        """ Initialize node's instance variables
        :complexity: O(1)
        """
        self.link = [None] * size
        self.frequency = frequency
        self.id = suffix_id
        self.level = lvl


class Trie:
    """ Represents a prefix / suffix trie which stores information as strings. Requires the Node class """

    def __init__(self):
        """ Initialize the root of a trie
        :complexity: O(1)
        """
        self.root = Node(frequency=0)

    def build_suffix_trie(self, key):
        """ Implemented for build_from_substrings
        Given a string, key, builds a suffix trie for it

        :complexity: O(K^2), where K is the length of the key
        """
        for char in range(len(key)):
            current = self.root
            for c in range(char, len(key) + 1):
                index = 0 if c == len(key) else ord(key[c]) - 97 + 1
                # if node does not exist, create node then traverse
                # otherwise just traverse
                if current.link[index] is None:
                    current.link[index] = Node(lvl=c, suffix_id=char)
                current = current.link[index]

    def search_longest_substring(self, key, char_unread):
        """ Implemented for build_from_substrings
        Given a string, key and an integer, the first unread character of a key,
        traverse the suffix trie to find the longest substring starting
        from that character in the suffix trie and returns a tuple
        in the form (substring_start_index, substring_end_index). If the first
        unread character does not exist in the trie, (None, None) is returned
        to indicate no such substring is found

        :complexity: O(L), where L is the longest suffix of the suffix trie
        """
        current = self.root
        char_index = ord(key[char_unread]) - 97 + 1

        # check if first unread character does not exist, straight away return None, None
        if current.link[char_index] is None:
            return None, None
        # otherwise continue to traverse the trie to find the longest substring
        else:
            while char_unread < len(key):
                char_index = ord(key[char_unread]) - 97 + 1
                # if next character does not exist, current character is the end of the substring
                if current.link[char_index] is None:
                    break
                else:
                    current = current.link[char_index]
                    char_unread += 1
            # current.id is the start index of the substring
            # current.level is the end index of the substring
            return current.id, current.level

    def insert_prefix(self, key):
        """ Implemented for alpha_pos
        Given a key, recursively traverses a prefix tree to insert a key
        by calling insert_prefix_aux

        :complexity: O(K), where K is the length of the key
        """
        current = self.root
        current.frequency += 1
        self.insert_prefix_aux(key, current)

    def insert_prefix_aux(self, key, current, char=0):
        """ Auxiliary function for insert_prefix, which inserts a key recursively
        into a prefix trie.

        :time complexity: O(K), where K is the length of the key
        """
        if char == len(key) + 1:  # no more characters to insert
            return
        else:
            index = 0 if char == len(key) else ord(key[char]) - 97 + 1
            # if node does not exist, create node with default frequency 1 then traverse it
            # otherwise just add its frequency by one then traverse
            if current.link[index] is None:
                current.link[index] = Node()
            else:
                current.link[index].frequency += 1
            self.insert_prefix_aux(key, current.link[index], char + 1)

    def sum_lexicographically_less(self, key):
        """ Implemented for alpha_pos
        Given a key, traverse a trie as far as possible, while summing up
        the frequency of all nodes lexicographically less than the current node,
        and returns the sum in the end

        :time complexity: O(K), where K is the length of the key
        """
        current = self.root
        sum_alpha_less = 0
        for i in range(len(key) + 1):
            index = 0 if i == len(key) else ord(key[i]) - 97 + 1
            # if node exists, add up the left branch frequencies then traverse: O(27)
            for j in range(index):
                if current.link[j] is not None:
                    sum_alpha_less += current.link[j].frequency
            if current.link[index] is not None:
                current = current.link[index]
            else:
                break
        return sum_alpha_less


def build_from_substrings(S, T):
    """ Given two non-empty lowercase strings, S and T, returns a list of
    tuples in the form of (substring_start_index, substring_end_index),
    which represents the smallest set of substrings
    of S that can be concatenated in order to obtain T, False is returned if
    it is not possible

    :time complexity: O(N^2 + M), where N is the number of characters in S
    and M is the number of characters in T
    """
    substring_list = []
    suffix_trie = Trie()

    # build suffix trie: O(N^2)
    suffix_trie.build_suffix_trie(S)

    # starting from the first character, traverse the trie to find the longest
    # possible substring, and repeat this starting from the subsequent first unread
    # character till all substrings are found to form T: O(M)
    char_to_read = 0
    while char_to_read < len(T):
        start, end = suffix_trie.search_longest_substring(T, char_to_read)
        if start is None:  # a character which is in T, but not in S is detected
            return False
        else:
            char_to_read += end - start + 1
            substring_list += [(start, end)]

    return substring_list


def alpha_pos(text, query_list):
    """ Given two lists of strings, text and query_list, returns a list of
    integers, where the i-th integer is represents the number of words in text
    which are alphabetically less than query_list[i]

    :time complexity: O(C + Q), where C is the total number of characters in text
    and Q is the total number of characters in query_list
    """
    # insert all words in text into a prefix trie: O(C)
    prefix_trie = Trie()
    for key in text:
        prefix_trie.insert_prefix(key)

    # traverse the trie using keys in the query_list
    # For every key, for every node that exists, add up all frequencies of nodes
    # (on the same level) which are lexicographically less than it: O(27 Q) = O(Q)
    output_list = [0] * len(query_list)
    index = 0
    for query in query_list:
        output_list[index] = prefix_trie.sum_lexicographically_less(query)
        index += 1
    return output_list

















