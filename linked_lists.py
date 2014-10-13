#! /usr/bin/python

# singly linked lists

class Node(object):
    def __init__(self, value, succ=None):
        self.value= value
        self.succ = succ
    def set_next(self, succ):
        self.succ = succ

class linked_list(object):
    """ Single linked list class. """

    def __init__(self, iterable):
        """ Make a linked list from an iterable.  """
        it = iter(iterable)
        try:
            self.first = Node(it.next())
        except StopIteration:
            return None
        end = self.first
        for item in it:
            end.set_next(Node(item))
            end = end.succ

    def __iter__(self):
        """ Traverse the list. """
        curr = self.first
        while curr is not None:
            yield curr.value
            curr = curr.succ

    def search(self, val):
        """ Return the node that contains the value val.
        If not found return None.
        """
        curr = self.first # current node
        while curr is not None:
            if curr.value == val:
                return curr
            curr = curr.succ
        return None # val is not found.

    def insert(self, val, node=None):
        """Insert a node with the value val behind node in a
        singly linked list. If the node parameter is not
        specified, insert at the beginning of the list.
        """
        if node == None:
            self.first = Node(val, succ=self.first)
            return
        right_node = node.succ
        new_node = Node(val, succ = right_node)
        node.set_next(new_node)

    def delete(self, node):
        """Delete node from the singly linked list l_list."""
        if node == self.first: # check first if the node is first
            self.first = node.succ
            return
        # find predecessor
        pred = self.first
        while pred.succ is not node:
            try: 
                pred = pred.succ
            except AttributeError:
                return # node is not in l_list, can't delete
        succ = node.succ # successor
        pred.succ = succ

class ll_tests:
    """
    >>> my_ll = linked_list(range(11))
    >>> my_ll.search(3).value
    3
    >>> my_ll.search(3).succ.value
    4
    >>> my_ll.insert(3.5,my_ll.search(3))
    >>> list(my_ll)
    [0, 1, 2, 3, 3.5, 4, 5, 6, 7, 8, 9, 10]
    >>> my_ll.insert(-1)
    >>> list(my_ll)
    [-1, 0, 1, 2, 3, 3.5, 4, 5, 6, 7, 8, 9, 10]
    >>> my_ll.delete(my_ll.search(3.5))
    >>> list(my_ll)
    [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> my_ll.delete(my_ll.search(-1))
    >>> list(my_ll)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    pass

if __name__=="__main__":
    import doctest
    doctest.testmod()
