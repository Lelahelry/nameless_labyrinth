from typing import Iterable

def pairwise(r: Iterable):
    it = iter(r)

    a = next(it)
    for b in it:
        yield (a, b)
        a = b