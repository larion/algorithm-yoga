#! /usr/bin/env python

""" Module for the abstract graph search/traversal function.

Clients can use this module to perform various search or traversal based graph
algorithms without having to worry about the internals.

The interface consists of one function (search), which performs highly
customizable graph traversals.

Alternatively clients can also use the GraphSearch class for more control.

Author: Larion Garaczi 
Date: 2014 
"""

from algoyoga_test import BaseTest
from collections import deque

# TODO:
# inorder, postorder, preorder
# implicit graphs!

def search(graph, node=None, search_type="bfs", 
        process_vertex=None, process_edge=None, new_component=None):
    """ A wrapper around GraphSearch.search() to perform graph searches. """
    mysearch = GraphSearch(graph, node, search_type, process_vertex,
            process_edge, new_component)
    return mysearch.search()

class GraphSearch(object):
    """ Class for graph traversals. The main public method of this class is
    search, which performs a traversal based on the way the GraphSearch object
    was initialized. 
    """
    def __init__(self, graph, node=None, search_type="bfs", 
        process_vertex=None, process_edge=None, new_component=None):
        """ Initialize graph search. The only mandatory argument is the graph
        itself, which is represented as a dictionary mapping nodes to the
        list of their neighbours.
        
        Node is the initial node to begin the traversal with (by default this
        is arbitrary). 

        Search type can either be "bfs" (Breadth First Search) or "dfs" (Depth
        First Search). "bfs" is the default.

        There are 3 functional parameters (all of them are optinal):
        - process_vertex(searchstate, vertex_id)
        - process_edge(searchstate, x, y)
        - new_component(searchstate, vertex_id) 

        In case any of these functions returns a value other than None, the
        search terminates with that value. The new_component function gets
        called whenever the traversal of one component is finished  and a new
        node outside of this component is found ready to be traversed (and also
        at the beginning of the search). The argument for new_component is the
        name of the first node of the new component. The parameter searchstate
        is a GraphSearchState object representing the current state of the
        search. """
        ### initialize search constants ###
        assert search_type in ["bfs", "dfs"]
        # initial node should be in the graph (when specified)
        assert node in graph if node else True 
        self.search_type=search_type
        # set all ommited processing functions to the placeholder
        # function do_nothing:
        def do_nothing(*args): 
            """ Do absolutely nothing. """
        if process_vertex is None: process_vertex=do_nothing
        if process_edge is None: process_edge=do_nothing
        if new_component is None: new_component=do_nothing
        self.process_vertex = process_vertex
        self.process_edge = process_edge
        self.new_component = new_component
        self.initial_node = node
        self.graph = graph

        ### initialize search state ###
        self.searchstate = self.get_search_state()

    def search(self):
        """ Traverse the graph. """ 
        state = self.searchstate
        # go through the nodes in the graph
        for node in state._to_process:
            if node in state.processed: 
                # already processed
                continue
            else:
                # traverse component
                newcomp = self.new_component(node)
                if newcomp is not None:
                    return newcomp
                state._push_node(node)
                while state.frontier:
                    # get node to process
                    current = state._pop_node()
                    # already processed - continue
                    if current in state.processed: 
                        continue
                    # process current vertex
                    # return if process_vertex() wants us to
                    proc_vertex = self.process_vertex(current)
                    if proc_vertex is not None:
                        return proc_vertex
                    for neighbour in self.graph[current]:
                        # process edge - return if process_edge() wants us to
                        proc_edge = self.process_edge(current, neighbour)
                        if proc_edge is not None:
                            return proc_edge
                        state._push_node(neighbour)
                    state.processed.add(current)
                    
    def get_search_state(self):
        """ Return a new GraphSearchState object. """
        return GraphSearchState(self.graph, self.initial_node, self.search_type)

class GraphSearchState(object):
    """ Class representing search states for GraphSearch. The main (public)
    attributes are (you will probably only need these): 
        
        processed    the set of nodes that are already processed by the search
        frontier    the current frontier (i. e. nodes that are discovered but
        not yet processed).
        
    object methods:
        
        _pop_node()   gets a single node from the frontier 
        _push_node(node)   pushes a single node to the frontier

    These methods are useful to abstract away from the underlying datastructure
    used for the frontier (i. e. a FIFO queue for BFS search and a stack for DFS
    search).  """

    def __init__(self, graph, initial_node, search_type):
        if search_type=="bfs":
            self.frontier = deque()
        elif search_type=="dfs":
            self.frontier = list()
        self._search_type = search_type
        self.processed = set()
        self._to_process = list()
        nodes = list(graph.iterkeys())
        if initial_node is not None:
            self._to_process.append(initial_node)
            nodes.remove(node)
        self._to_process.extend(nodes)

    def _pop_node(self):
        """ Pop node from frontier. """
        if self._search_type=="bfs":
            return self.frontier.popleft()
        elif self._search_type=="dfs":
            return self.frontier.pop()

    def _push_node(self, node):
        """ Push node to frontier. """
        self.frontier.append(node)

class GraphSearchTest(BaseTest):
    def __init__(self):
        testlist = [self.test_search]
        super(GraphSearchTest,self).__init__("graph traversal", testlist)

    def test_search(self):
        """ test the search (bfs + dfs traversal of graphs) function """
        tree = { # test case 1 - a tree
                1: [2, 3],
                2: [4, 5],
                3: [9],
                4: [6, 7],
                5: [8],
                6: [],
                7: [],
                8: [],
                9: [10, 11],
                10: [],
                11: [],
                }
        cycle = { # test case 2 - a 4-cycle
                1: [2],
                2: [3],
                3: [4],
                4: [1],
                }
        trivial_graph = dict() # test case 3 - empty graph
        # assume postorder traversal
        tree_bfsorder = [1, 2, 3, 4, 5, 9, 6, 7, 8, 10, 11]
        tree_dfsorder = [1, 3, 9, 11, 10, 2, 5, 8, 4, 7, 6]
        tree_expected = {"bfs": tree_bfsorder, "dfs": tree_dfsorder}
        cycle_expected = {"bfs": [1,2,3,4], "dfs": [1,2,3,4]}
        trivial_expected = {"bfs": list(), "dfs": list()}
        listing = []
        testcases = [(tree, tree_expected), (cycle, cycle_expected), (trivial_graph, trivial_expected)]
        def collect_nodes(node):
            listing.append(node)
        for mode in ["bfs", "dfs"]:
            for testobject, expected in testcases:
                search(testobject, process_vertex = collect_nodes, search_type=mode)
                assert listing == expected[mode]
                del listing[:]
        return "test pass"

if __name__ == "__main__":
    tester = GraphSearchTest()
    tester.run_tests()
