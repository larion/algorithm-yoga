#! /usr/bin/env python

""" Miscellaneous graph algorithms.

The algorithms that are implemented in this module are:
    c_com(graph) - find the connected components in an undirected graph

    scc(graph) - find all strongly connected components in an directed graph

    cycles(graph) - find all cycles in an undirected graph

    rand_graph(n, p) - return a random undirected graph and
    an edge probability of p (0 <= p <= 1)

    rand_dgraph(n, p) - return a random directed graph with n nodes and
    an edge probability of p (0 <= p <= 1)

Author: Larion Garaczi
Date: 2014
"""
import random
import graphsearch

from algoyoga_test import BaseTest

### interface ###

def cycles(input_graph):
    """ Wrapper around Graph.cycles """
    gr = Graph(input_graph)
    return gr.cycles()

def c_com(input_graph):
    """ Wrapper around Graph.c_com """
    gr = Graph(input_graph)
    return gr.c_com()

def scc(input_graph):
    """ Wrapper around Graph.scc """
    gr = Graph(input_graph)
    return gr.scc()

def rand_graph(n, p):
    """ Generate a random undirected graph with n nodes and an
    edge probability of p.
    """
    graph = defaultdict(list)
    for i in range(n):
        graph[i] = graph[i] #initialize it!
        for i2 in range(i+1, n):
            if random.random()<=p:
                graph[i].append(i2)
                graph[i2].append(i)
    return graph

def rand_dgraph(n, p):
    """ Generate a random directed graph with n nodes and an
    edge probability of p.
    """
    graph = dict()
    for i in range(n):
        graph[i]=[]
        for i2 in range(n):
            if random.random()<=p:
                graph[i].append(i2)
    return graph

#################

# TODO
# kruskal(graph) - find the minimum spanning tree (for sparse graphs)
#
# prim(graph) - find the minimum spanning tree (for dense graphs)
#
# largest_perm(graph) - find the maximum permutation in a bipartite graph
#
# color(graph, n) - find an n-coloring for the graph
#
# shortest_path(graph, x, y) - find the shortest path between the nodes
# x and y in an unweighted graph
#
# dijkstra(graph, x, y) - find the shortest path between two nodes in a
# weighted graph
#
# bellman_ford(graph, x, y) - find the shortest path between two nodes in a
# weighted graph
#
# floyd_warshall(graph) - find the shortest path between all pairs in a graph
#
# diameter(graph) - find the diameter of a graph
#
# transitive_closure(graph) - return the transitive closure of the graph
#
# articulaton_vertex(graph) - find the articulation vertices in a graph
#

# TODO
def largest_perm(graph): #TODO: update docstring -> relation between natural numbers
    """ Takes an arbitrary relation R in {1, 2, ..., n}^2. The relation is represented as a
    tuple (a_1, a_2, a_3) where a_n is the list of numbers m for which Rnm. Return the
    largest subrelation that represents a permutation of some subset L of {1, 2, ..., n}.
    (Or - equivalently - return the largest bijection which is also a subrelation of R.)
    """ 
    perm = graph[:]
    counts = [len([n_list for n_list in graph if n in n_list]) for n in range(len(graph))]
    print(counts)
    try:
        next_ind = counts.index(0)
    except ValueError:
        return perm
    while True:
        n_list = perm[next_ind]
        for neighbour in n_list:
            counts[neighbour]-=1
        del perm[next_ind]
        try:
            next_ind = counts.index(0)
        except ValueError:
            return perm

class Graph(object):
    """ Class for the graph algorithms. """
    def __init__(self, graph):
        """ Initialize the Graph object. This method just stores the graph to be
        processed.
        """
        self.graph = graph

    def scc(self):
        """ Take a directed graph represented as an adjacency list (a dict
        mapping vertices to their neighbours) and return its strongly
        connected components.
        """
        class searchglobals:
            clock = 0 # initialize clock
            dt = dict() # map nodes to their discovery time
            # map a node X to the lowest dt[Y] s. t. Y is reachable from X
            reachable_dt = dict()
            stack = []
            components = list()

        def proc_vertex_early(s_state, node):
            # initialize dt and reachable_dt (every node is trivially reachable from itself)
            searchglobals.reachable_dt[node] = searchglobals.dt[node] = searchglobals.clock
            searchglobals.clock+=1 # tick
            searchglobals.stack.append(node)

        def proc_edge(s_state, x, y):
            if y in s_state.discovered and y not in s_state.processed:
                # found back-edge, update reachable_dt accordingly
                if searchglobals.reachable_dt[x] > searchglobals.dt[y]:
                    searchglobals.reachable_dt[x] = searchglobals.dt[y]

        def proc_vertex_late(s_state, node):
            parent = s_state.parents[node]
            reachable = searchglobals.reachable_dt[node]
            dt = searchglobals.dt[node]
            # propagate reachable_dt upwards
            if parent is not None and reachable < searchglobals.reachable_dt[parent]:
                searchglobals.reachable_dt[parent] = reachable
            if reachable == dt:
                # found a component, pop it out from the stack
                comp = set()
                comp_node = searchglobals.stack.pop()
                comp.add(comp_node)
                while comp_node != node:
                    comp_node = searchglobals.stack.pop()
                    comp.add(comp_node)
                searchglobals.components.append(comp)

        graphsearch.search(self.graph, search_type="dfs", process_vertex_early = proc_vertex_early,
                process_edge = proc_edge, process_vertex_late = proc_vertex_late)
        return searchglobals.components

    def cycles(self):
        """ Return the cycles in an undirected graph. """
        graph = self.graph
        cycles = []
        def process_edge(s_state, x, y):
            cycle = []
            if y in s_state.discovered and y not in s_state.processed and s_state.parents[x] != y:
                # We found a back edge; now we just need to back up from y until
                # we find x to get the cycle
                # print x, y
                z = x
                while z!=y:
                    cycle.append(z)
                    z=s_state.parents[z]
                cycle.append(y)
                cycles.append(list(reversed(cycle)))
        graphsearch.search(graph, search_type="dfs", process_edge = process_edge)
        return cycles

    def c_com(self):
        """ Take an undirected graph represented as an adjacency list (a dict)
        and return its connected components (as a list of sets).
        """
        graph = self.graph
        comp_members = set() # current component members
        comps = [] # list containing all the components
        def push_stack(s_state, node):
            comp_members.add(node)
        def pop_stack(s_state, node):
            component = comp_members.copy()
            comp_members.clear()
            if component: # a component can't be empty
                comps.append(component) # add component to the component list
        graphsearch.search(graph, search_type="bfs", process_vertex_early = push_stack, new_component = pop_stack)
        pop_stack(None, None) # add the last component
        return comps

class GraphTest(BaseTest):
    def __init__(self):
        testlist = [self.test_ccom, self.test_cycles, self.test_scc]
        super(GraphTest,self).__init__("miscellaneous graph algorithms", testlist)

    def test_scc(self):
        """ Test the scc function (strongly connected components). """
        complex_graph = {
                1: [2], # first scc
                2: [3, 5],
                3: [4],
                4: [1],
                5: [6, 7], # second scc
                6: [5, 7],
                7: [8], # third scc
                8: [9], # fourth scc
                9: [10],
                10: [8],
                11: [12], # fifth scc
                12: [], # sixth scc
                13: [14], # seventh scc
                14: [13],
                }
        complex_sccs = frozenset([
                frozenset([1,2,3,4]),
                frozenset([5,6]),
                frozenset([7]),
                frozenset([8,9,10]),
                frozenset([11]),
                frozenset([12]),
                frozenset([13,14]),
                ])
        triv = dict()
        triv_sccs = frozenset()
        large_cycle = {n:[(n+1)%100] for n in range(100)}
        large_cycle_sccs = frozenset([frozenset(range(100))])
        testcases = [
                (complex_graph, complex_sccs),
                (triv, triv_sccs),
                (large_cycle, large_cycle_sccs),
                ]
        for (input_graph, expected) in testcases:
            result = scc(input_graph)
            assert frozenset([frozenset(component) for component in result]) == expected
        return "test pass"

    def test_ccom(self):
        """ test c_com (connected components in an undirected graph) function """
        # a graph with 4 connected components
        testgraph = {
                1: [2],
                2: [1,3],
                3: [2],
                4: [5,6,7],
                5: [4,6,7],
                6: [4,5,7],
                7: [4,5,6],
                8: [9],
                9: [8],
                10: [],
                }
        assert c_com(testgraph)==[set([1, 2, 3]), set([4, 5, 6, 7]), set([8, 9]), set([10])]

        # edge case - empty graph
        testgraph2 = dict()
        assert c_com(testgraph2)==[]

        # large complete graph
        testgraph3 = {n: range(100) for n in range(100)}
        assert c_com(testgraph3) == [set(range(100))]
        return "test pass"

    def test_cycles(self):
        """ Test the cycles function. """
        testcycle0 = dict()
        testcycle1 = {n: [(n-1)%100, (n+1)%100] for n in range(100)}
        testcycle2 = dict()
        testcycle2 = {n: [n-1, n+1] for n in range(1,100)}
        testcycle2[0] = [1]
        # make a cycle
        testcycle2[100] = [99, 80]
        testcycle2[80].append(100)
        testcycle3 = {1: [1]}
        testcycle4 = {
                0: [1, 3],
                1: [0, 2],
                2: [1, 3, 4],
                3: [0, 2],
                4: [2, 7, 5],
                5: [4, 6],
                6: [5, 7],
                7: [4, 6],
                }
        cycle4_expected = [set([0,1,2,3]), set([4,5,6,7])]
        cycle4_results = [set(cycle) for cycle in cycles(testcycle4)]
        assert cycles(testcycle0) == []
        assert set(cycles(testcycle1)[0])== set(range(100))
        assert set(cycles(testcycle2)[0])== set(range(80, 101))
        assert cycles(testcycle3) == [[1]]
        assert all(cycle in cycle4_results for cycle in cycle4_expected)
        assert all(cycle in cycle4_expected for cycle in cycle4_results)
        return "test pass"

if __name__ == "__main__":
    tester = GraphTest()
    tester.run_tests()
