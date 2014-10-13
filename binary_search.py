#! /usr/bin/python

def binary_search(lst, item):
    """ Perform binary search on a sorted list. 
    Return the index of the element if it is in
    the list, otherwise return -1.
    """
    low = 0
    high = len(lst) - 1
    while low < high:
        middle = (high+low)/2
        current = lst[middle]
        if current == item:
            return middle
        elif current < item:
            low = middle+1
        elif current > item:
            high = middle-1
    if lst[low] == item:
        return low
    return -1

class unit_test:
    """ 
    >>> binary_search(range(1000), 547)
    547
    >>> binary_search(range(1000), 999)
    999
    >>> binary_search(range(1000), 0)
    0
    >>> binary_search(range(1000), 1000)
    -1
    >>> binary_search(range(1000), -1)
    -1
    >>> binary_search([1,1,1,1,1,2,2,2], 2) > 4
    True
    >>> 5 > binary_search([1,1,1,1,1,2,2,2], 1) > -1
    True
    >>> binary_search([1,1,1,1,1,2,2,2], 3)
    -1
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
