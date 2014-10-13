#! /usr/bin/python

from random import randrange
from collections import defaultdict

def randlist(n, n2=1000):
    """ generate a random list of length n """
    return [randrange(0,n2) for _ in range(n)]

def s_sort(seq):
    """ perform selection sort """
    for i in range(len(seq)-1,0,-1):
        max_i = i
        for i2 in range(0, i):
            if seq[i2]>seq[max_i]:
                max_i = i2
        seq[i], seq[max_i] = seq[max_i], seq[i]

def s_sort_rec(seq, i=None):
    """ perform selection sort recursively """
    if i is None:
        i = len(seq)-1
    if i == 0:
        return
    max_ind, _ = max(enumerate(seq[0:i+1]), key=lambda x: x[1])
    seq[max_ind], seq[i] = seq[i], seq[max_ind]
    s_sort_rec(seq, i-1)

def i_sort(seq):
    """ perform insertion sort """
    for i in range(1, len(seq)):
        val = seq[i]
        del seq[i]
        seq.insert(0, val)
        i2 = 0
        while i2 < i and seq[i2+1]<seq[i2]:
            seq[i2], seq[i2+1] = seq[i2+1], seq[i2]
            i2+=1

def i_sort_rec(seq, i=None):
    """ perform insertion sort recursively"""
    if i is None:
        i=len(seq)
    if i==1:
        return
    i_sort_rec(seq, i-1)
    val = seq[i-1]
    del seq[i-1]
    seq.insert(0, val)
    i2 = 0
    while i2 < i-1 and seq[i2+1]<seq[i2]:
        seq[i2], seq[i2+1] = seq[i2+1], seq[i2]
        i2+=1

def count_sort(seq):
    """ perform count sort and return sorted sequence without
    affecting the original
    """
    counts = defaultdict(list)
    for elem in seq:
        counts[elem].append(elem)
    result = []
    for i in range(min(seq), max(seq)+1):
        result.extend(counts[i])
    return result


