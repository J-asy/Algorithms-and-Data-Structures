""" This file contains a suffix array generator.
The suffix array is obtained by building a suffix tree (with ukkonen's algorithm) then traversing it.
"""

import sys


class Node:
    ALPHABET_OFFSET = 97

    def __init__(self, node_id=None, alpha_size=26):
        """ Default alphabet set includes ASCII characters a - z, with special terminal symbol $ """
        self.edges = [None] * (alpha_size + 1)
        self.leaf = True
        self.id = node_id

    def get_edge(self, character):
        """ Given a character, returns edge that links up to the corresponding child node """
        return self.edges[Node.calc_index(character)]

    def connect(self, character, text_start, text_end, node_id):
        """ Adds a new edge that links up to another node corresponding to character specified """
        new_node = Node(node_id)
        new_edge = Edge(text_start, text_end, new_node)
        self.edges[Node.calc_index(character)] = new_edge
        self.leaf = False

    def set_id(self, new_id):
        self.id = new_id

    def get_id(self):
        return self.id

    def is_leaf(self):
        return self.leaf

    def set_not_leaf(self):
        self.leaf = False

    @staticmethod
    def calc_index(char):
        """ Given a character, returns its corresponding index for the edges array """
        return 0 if char == "$" else ord(char) - Node.ALPHABET_OFFSET + 1


class Edge:
    def __init__(self, text_start, text_end, next_node):
        self.text = text_start, text_end
        self.next = next_node

    def __len__(self):
        return self.text[1].get_end() - self.text[0] + 1

    def next_node(self):
        return self.next

    def insert(self, character, insert_point):
        """ Breaks an edge into two by inserting a new node in the middle
        and returns the internal node. Original substring represented by
        two nodes and one edge becomes three nodes and two edges.

        :time complexity: O(1)
        """
        old_node = self.next
        remaining_edge = Edge(insert_point + 1, self.text[1], old_node)
        self.update_text(self.text[0], End(insert_point))  # shortens old edge

        # links internal node with the remaining edge
        internal_node = Node()
        internal_node.set_not_leaf()
        internal_node.edges[Node.calc_index(character)] = remaining_edge
        self.next = internal_node

        return self.next

    def get_text(self):
        return self.text

    def update_text(self, text_start, text_end):
        """ Typically used for shortening an edge """
        self.text = text_start, text_end


class End:
    def __init__(self, end):
        self.end = end

    def increment_end(self):
        self.end += 1

    def decrement_end(self):
        self.end -= 1

    def get_end(self):
        return self.end


class Tree:
    def __init__(self, ref_text=""):
        self.root = Node()
        self.ref_text = ref_text + "$"
        self.global_end = End(-1)

    def get_root(self):
        return self.root

    def get_edge(self, active_node, txt_ptr):
        """ Gets an edge of the node that corresponds to
        the character of ref_text, that is referred to by txt_ptr
        """
        return active_node.get_edge(self.refer(txt_ptr))

    def refer(self, ref_index):
        return self.ref_text[ref_index]

    def skip_count(self, active_node, active_length, txt_ptr, txt_end):
        """ Skips through nodes and edges using using active_length,
        to return the appropriate pointers to a point in the tree that
        explicit character comparison needs to begin from

        :param active_node: current active node
        :param active_length: number of known matching characters that we can skip through;
                            length defined from the start of the root
        :param txt_ptr: j
        :param txt_end: i
        :return: new active_node, new active edge, index of character to begin explicit comparison
                in self.ref_text, remaining active_length that is too short to skip through a node

        :time complexity: O(m), where m is the number of nodes of the longest path in the tree
        :space complexity: O(1)
        """
        n = len(self.ref_text)
        active_edge = None

        if txt_ptr < n:
            active_edge = self.get_edge(active_node, txt_ptr)

            if active_edge is not None and active_length >= len(active_edge) and txt_ptr + len(active_edge) <= txt_end:
                active_length -= len(active_edge)
                txt_ptr += len(active_edge)

                # while the number of remaining known matching characters is
                # still sufficient to get skip the entire edge
                while active_length >= 0 and txt_ptr <= txt_end:
                    active_node = active_edge.next_node()
                    active_edge = self.get_edge(active_node, txt_ptr)
                    if active_edge is None or active_length < len(active_edge):
                        break
                    else:
                        active_length -= len(active_edge)
                        txt_ptr += len(active_edge)

        return active_node, active_edge, txt_ptr + active_length, active_length

    def traveller(self, catch_up, active_node, active_edge, remaining, txt_ptr):
        """ Does explicit character comparison while no mismatch is found, traverses through
        nodes in the way if needed. Incorporates Rule 3 & showstopper.

        :param catch_up: Indicates how far j is behind i, used to know when it is ok to increment i
                        if j catches up to i eventually during explicit character comparison
        :param active_node: current active node
        :param active_edge: current active edge
        :param remaining: The number of characters that can be skipped on the current edge
        :param txt_ptr: The position to start explicit character comparison in self.ref_text

        :time complexity: O(k), where k is the number of characters left from txt_ptr to the end of self.ref_text
        :space complexity: O(1)
        """
        n = len(self.ref_text)
        i = self.global_end
        mismatch = False
        reached_node = False  # True if just reached node cannot even find next edge to compare, False otherwise
        edge_ptr = remaining + active_edge.get_text()[0]
        total_matched_char = 0  # total number of matching characters during explicit comparison
        matched_char = 0  # number of matching characters starting from current active node

        while edge_ptr <= i.get_end() and not mismatch and txt_ptr < n:
            if self.refer(edge_ptr) == self.refer(txt_ptr):
                reached_node = False
                edge_ptr += 1
                txt_ptr += 1
                matched_char += 1

                # showstopper
                if txt_ptr > i.get_end() and i.get_end() + 1 < n:
                    i.increment_end()
                    catch_up += 1

                # traverse next node if reached the end of the edge
                if active_edge.get_text()[1].get_end() < edge_ptr <= i.get_end() and txt_ptr < n:
                    total_matched_char += matched_char
                    reached_node = True
                    active_node = active_edge.next_node()
                    active_edge = self.get_edge(active_node, txt_ptr)
                    if active_edge is None:
                        break
                    edge_ptr = active_edge.get_text()[0]
                    matched_char = 0
            else:
                mismatch = True

        return txt_ptr, catch_up, active_node, active_edge, matched_char, total_matched_char, reached_node

    def generate_suffix_array(self, current=None, suffix_array=None):
        """ Retrieve suffix id from the leaves in pre-order sequence to generate
        suffix array from the suffix tree

        :time complexity: O(n), where n is the number of nodes in the tree
        :space complexity: O(l), where l is the number of leaves in the tree
        """
        if current is None:
            current = self.root
            suffix_array = []
            return self.generate_suffix_array(current, suffix_array)
        else:
            if current.is_leaf():
                suffix_array.append(current.get_id())

            for edge in current.edges:
                if edge is not None:
                    next_node = edge.next_node()
                    self.generate_suffix_array(next_node, suffix_array)
            return suffix_array

    @staticmethod
    def ukkonen(string):
        """ ALMOST ukkonen implementation to build a suffix tree,
        with all rules and tricks, except suffix links

        :time complexity: O(n**2), since i and j outer loops are O(2n)
        and skip count still loosely bounded by O(n), where n is the length of the string
        :space complexity: O(nc), where c is the alphabet size of the tree
        and n is the length of the string
        """
        suffix_tree = Tree(string)
        i = suffix_tree.global_end
        j = active_length = catch_up = 0  # active_length defined from the root
        n = len(suffix_tree.ref_text)

        i.increment_end()
        while i.get_end() < n:
            while j <= i.get_end() and j < n:
                active_node = suffix_tree.get_root()
                active_edge = active_node.get_edge(suffix_tree.refer(j))
                pseudo_j = j
                remaining = 0

                # skip count to locate new character to compare
                if active_length > 0:
                    active_node, active_edge, pseudo_j, remaining = suffix_tree.skip_count(active_node, active_length,
                                                                                           j, i.get_end())
                    pseudo_j = min(pseudo_j, n - 1)

                if active_edge is None:
                    insert_node = active_node
                    insert_node_index = min(i.get_end(), pseudo_j, n - 1)
                    active_length = max(active_length - 1, 0)
                    catch_up = max(catch_up - 1, 0)
                else:
                    # call traveller to compare characters explicitly as far as possible;
                    # traveller increments i if necessary: Rule 3 + showstopper
                    last_catch_up = j == i.get_end()
                    catch_up = 0 if last_catch_up else catch_up - 1
                    txt_ptr, catch_up, active_node, active_edge, matched_char, total_matched_char, reached_node = \
                        suffix_tree.traveller(catch_up, active_node, active_edge, remaining, pseudo_j)

                    # Rule 2: break edge if mismatch occurs in the middle of an edge;
                    # otherwise will be Rule 2: clean insert only
                    if not reached_node:
                        # insert internal node in existing edge
                        old_edge_start = active_edge.get_text()[0]
                        if matched_char == 0:
                            old_edge_index = old_edge_start + max(remaining - 1, 0)
                        else:
                            old_edge_index = old_edge_start + matched_char - 1

                        internal_node = active_edge.insert(suffix_tree.refer(old_edge_index + 1), old_edge_index)
                        insert_node = internal_node
                    else:
                        insert_node = active_node

                    insert_node_index = min(txt_ptr, n - 1)

                    # update active length
                    if i.get_end() == j:
                        active_length = 0
                    elif last_catch_up and catch_up > 0:
                        active_length = total_matched_char - 1
                    # j lags behind i at the start of the iteration
                    # but then manages to catch up and matches characters exceeding i
                    elif not last_catch_up and catch_up > 0 and total_matched_char > active_length:
                        active_length += total_matched_char - 1
                    else:
                        active_length = max(active_length - 1, 0)

                # Rule 2: clean insert
                insert_node.connect(suffix_tree.refer(insert_node_index), insert_node_index, i, j)

                # Rule 1: extend leaf
                if i.get_end() == j:
                    i.increment_end()

                j += 1

        i.decrement_end()
        return suffix_tree


def ukkonen_driver(file_name):
    """ Reads a string from the specified file, then generates a suffix array
    for it using a suffix_tree and writes it into output_suffix_array.txt
    """
    with open(file_name) as input_file:
        contents = input_file.read().strip()

    suffix_tree = Tree.ukkonen(contents)
    suffix_array = suffix_tree.generate_suffix_array()

    with open("output_suffix_array.txt", "w") as output_file:
        output_file.write(str(suffix_array[0]))
        for num in range(1, len(suffix_array)):
            output_file.write("\n" + str(suffix_array[num]))


if __name__ == "__main__":
    filename = sys.argv[1]
    ukkonen_driver(filename)



