#! /usr/bin/python

def uniq(lst):
    """ Take a sorted list and return a list with
    duplicates removed. Also return the length of
    the contracted list:

    >>> uniq([1,3,7,7,8,9,9,9,10])
    ([1, 3, 7, 8, 9, 10], 6)
    >>> uniq([1,1,1,1,1,1,1,1])
    ([1], 1)
    >>> uniq([1,1,1,2,2,3,3,3])
    ([1, 2, 3], 3)
    >>> uniq([1,3,7])
    ([1, 3, 7], 3)
    """
    lst2 = lst[:]
    last = lst2[0]
    i=1
    while i<len(lst2):
        current = lst2[i]
        if current == last:
            del lst2[i]
        else:
            last = current
            i+=1
    return (lst2, len(lst2))

def rotate_list(lst, N):
    """ Returns the input list rotated by N positions.

    >>> rotate_list([1,2,3,4,5,6], 2)
    [5, 6, 1, 2, 3, 4]
    >>> rotate_list([1,2,3,4,5,6], 5)
    [2, 3, 4, 5, 6, 1]
    >>> rotate_list([1,2,3,4,5,6], 18)
    [1, 2, 3, 4, 5, 6]
    """
    lst2 = []
    length = len(lst)
    offset = length-N
    for ind in xrange(length):
        pos = (ind+offset)%length
        lst2.append(lst[pos])
    return lst2

if __name__ == "__main__":
    import doctest
    doctest.testmod()

