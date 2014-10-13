#! /usr/bin/env python

""" Miscellaneous graph algorithms.

The algorithms that are implemented in this module are:
    c_com(graph) - find the connected components in an undirected graph

    rand_graph(n, p) - return a random undirected graph and 
    an edge probability of p (0 <= p <= 1)

    rand_dgraph(n, p) - return a random directed graph with n nodes and 
    an edge probability of p (0 <= p <= 1)

Author: Larion Garaczi
Date: 2014
"""
    # TODO
    # scc(graph) - find the strongly connected components of a directed graph
    #
    # kruskal(graph) - find the minimum spanning tree (for sparse graphs)
    #
    # prim(graph) - find the minimum spanning tree (for dense graphs)
    #
    # cycles(graph) - find cycles in a graph
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
    # articulaton_vertex(graph) - find the articulation vertices in a graph
    #

import random
import graphsearch

from algoyoga_test import BaseTest

def c_com(graph):
    """ Take an undirected graph represented as an adjacency list (a dict)
    and return its connected components (as a list of sets).
    """
    comp_members = [] # current component members
    comps = [] # list containing all the components

    def push_stack(node):
        comp_members.append(node)

    def pop_stack(node):
        component = comp_members[:]
        del comp_members[:]
        if component: # a component can't be empty
            comps.append(set(component)) # add component to the component list

    graphsearch.search(graph, process_vertex = push_stack, new_component = pop_stack)
    pop_stack(None) # add the last component
    return comps


def rand_graph(n, p):
    """ generate a random undirected graph with n nodes and an
    edge probability of p
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
    """ generate a random directed graph with n nodes and an
    edge probability of p 
    """
    graph = dict()
    for i in range(n):
        graph[i]=[]
        for i2 in range(n):
            if random.random()<=p:
                graph[i].append(i2)
    return graph

# TODO
def largest_perm(graph): #TODO: update docstring -> relation between natural numbers
    """ Takes an arbitrary relation R in {1, 2, ..., n}^2. The relation is represented as a
    tuple (a_1, a_2, a_3) where a_n is the list of numbers m for which Rnm. Return the
    largest subrelation that represents a permutation of some subset L of {1, 2, ..., n}.
    Or equivalently return the largest bijection, which is a subrelation of R.
    """ 
    perm = graph[:]
    counts = [len([n_list for n_list in graph if n in n_list]) for n in range(len(graph))]
    print counts
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

class GraphTest(BaseTest):
    def __init__(self):
        testlist = [self.test_ccom]
        super(GraphTest,self).__init__("miscellaneous graph algorithms", testlist)

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

if __name__ == "__main__":
    tester = GraphTest()
    tester.run_tests()
