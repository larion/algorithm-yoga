#! /usr/bin/python

import random
import itertools
import math

def string_hash(text, mod):
    """ Return a hash value for an ASCII string. The value will be
    between 0 and mod-1. It is advisable to use a prime number
    for mod to guarantee a fairly uniform distribution. """
    base = 256 # size of the alphabet (ASCII)
    numstr = [ord(char) for char in text]
    length = len(numstr)
    hashval = 0
    assert all(0 <= num < base for num in numstr)
    for ind, val in enumerate(numstr):
        hashval += base ** (length-ind-1)*val
        hashval %= mod
    return hashval

def rk_search(text, pattern): 
    """ Return the index of pattern in text if it is found.
    Otherwise return None. This uses the Rabin-Karp algorithm.
    >>> rk_search("foobar", "ob")
    2
    >>> rk_search("foobar", "foo")
    0
    >>> rk_search("foobar", "f")
    0
    >>> rk_search("foobar", "bar")
    3
    >>> rk_search("foobar", "r")
    5
    >>> rk_search("a"*1000+"b"*1000, "ab")
    999
    >>> rk_search("a"*1000+"b"*1000, "a"*1000)
    0
    >>> rk_search("a"*1000+"b"*1000, "a"*1001) is None
    True
    >>> rk_search("a"*10000, "aaaaab") is None
    True
    """
    length = len(text)
    wlength = len(pattern) # length of the window
    # ensure that there are not too many collisions on average:
    hashmod = next(generate_primes(length))
    def hashstr(inp): return string_hash(inp, hashmod)
    pathash = hashstr(pattern)
    currhash = hashstr(text[:wlength]) # hash of first window
    base = 256 # assume ASCII
    for ind in range(1, length - wlength + 1): # loop through the windows
        # Use lazy evaluation to avoid frequent comparisons.
        if currhash == pathash and text[ind-1:ind+wlength-1] == pattern: 
            return ind-1
        new_ord = ord(text[ind+wlength-1]) # the new character in the window
        old_ord = ord(text[ind-1]) # the character that is no longer in window
        # Update hash in O(1) time:
        currhash = base*(currhash - old_ord*base**(wlength-1))+new_ord
        currhash %= hashmod
    if currhash == pathash and text[length-wlength:]==pattern:
        return length-wlength
    return None
        
def generate_primes(start):
    """ generate primes in increasing order, starting from 
    the number start. 
    >>> generator = generate_primes(2)
    >>> [generator.next() for _ in xrange(10)] # first 10 primes
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    >>> generator = generate_primes(100)
    >>> # first 10 primes over 100
    >>> [generator.next() for _ in xrange(10)] 
    [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
    """
    for n in itertools.count(start): 
        # check if n is a prime
        maxdivisor = int(math.floor(math.sqrt(n))) # maximum possible divisor
        for div_cand in range(2, maxdivisor+1):
            if n%div_cand==0:
                break # n is not a prime, continue searching
        else: # no divisors -> n is a prime
            yield n


def unit_test():
    # check if string_hash makes fairly evenly distributed hashes
    bigprime = 10007
    hashes = []
    for _ in range(1000):
        randstring = "".join([chr(random.randrange(256)) for _ in range(random.randrange(1,30))])
        hashes.append(string_hash(randstring, bigprime))
    collisions = 1000 - len(set(hashes))
    assert collisions < 100
    print "tests pass."
    return True
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    unit_test()
