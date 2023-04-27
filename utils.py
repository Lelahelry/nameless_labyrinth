from typing import Iterable

def two_by_two(r: Iterable):
    it = iter(r)

    a = next(it)
    for b in it:
        yield (a, b)
        a = b