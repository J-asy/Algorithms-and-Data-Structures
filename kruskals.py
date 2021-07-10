""" Kruskal's algorithm implemented using union by rank with path splitting

Call kruskals_driver to run the program.

Arguments:
num_vertices - The total number of vertices

file - A plain text file. Every line in the text file contains
single edge with weight w connecting vertex u to vertex v
in G represented by 3 integers in the following format:
u v w

Returns a file where:
- the total weight of a minimum spanning tree is on the first line.
- each subsequent line is an edge in the minimum weight spanning tree, in the
same format as the input file.
"""


class Disjoint_set:
    def __init__(self, size):
        """ Initializes the parent array, at the beginning all nodes are roots

        :time complexity: O(size)
        :space complexity: O(size)
        """
        self.parent_array = [-1] * size

    def find(self, target):
        """ Find the parent of the target, while doing path splitting along the way

        :time complexity: O(log_2 N), where N is the number of nodes in the set
        :amortised time complexity: O(1) due to path splitting
        :space complexity: O(1)
        """
        grandchild = target

        while self.parent_array[target] >= 0:
            # path splitting
            self.parent_array[grandchild] = self.parent_array[target]
            grandchild = target

            # find next parent
            target = self.parent_array[target]
        return target

    def union_by_rank(self, u, v):
        """ Given nodes represented by u and v, merges the smaller tree
        under the larger tree by updating the parent array appropriately

        :time complexity: O(log_2 N), where N is the number of nodes in the set
        :amortised time complexity: O(1) due to path splitting
        :space complexity: O(1)
        """

        # finding parent takes O(log_2 N) time for worst case
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            rank_u = -1 * self.parent_array[root_u]
            rank_v = -1 * self.parent_array[root_v]

            if rank_u > rank_v:
                self.parent_array[root_v] = root_u
            elif rank_v > rank_u:
                self.parent_array[root_u] = root_v
            else:
                self.parent_array[root_u] = root_v
                self.parent_array[root_v] = -1 * (rank_v + 1)
            return True

        return False


def get_weight(item):
    return item[-1]


def kruskals(num_vertices, edges_list):
    """ Given a connected graph in the form of an integer specifying the
    number of vertices and a list of edges, finds its minimum spanning tree
    using union by rank with path splitting

    :time complexity: O(E log E),
    :space complexity: O(E), where E is the number of edges in edges_list
    """
    # sort all edges by weight in ascending order
    edges_list.sort(key=get_weight)

    disjoint_set = Disjoint_set(num_vertices)
    included_edges = []
    total_weight = 0
    i = 0

    # Union by rank while haven't found all edges
    while len(included_edges) < num_vertices - 1:
        current_u, current_v, weight = edges_list[i]
        merged = disjoint_set.union_by_rank(current_u, current_v)

        if merged:
            included_edges.append(edges_list[i])
            total_weight += weight
        i += 1

    return total_weight, included_edges


def kruskals_driver(num_vertices, file):
    f = open(file, "r")
    contents = f.read().splitlines()
    edges_list = []
    for line in contents:
        edge = [int(x) for x in line.split()]
        edges_list.append(edge)
    f.close()

    weight, output_list = kruskals(num_vertices, edges_list)

    f = open("output_kruskals.txt", "w")
    f.write(str(weight))
    for edge in output_list:
        f.write("\n" + str(edge[0]) + " " + str(edge[1]) + " " + str(edge[2]))
    f.close()


