# -*- coding: utf-8 -*-

from typing import Iterable, Callable, Iterator, TypeVar

T = TypeVar('T')

def pairwise(r: Iterable[T]) -> Iterator[tuple[T, T]]:
    it = iter(r)

    a = next(it)
    for b in it:
        yield (a, b)
        a = b

def bfs_walk(origin: T, adjacency_fn: Callable[[T], Iterator[T]]) -> Iterator[list[T]]:
    queue = [[origin]]
    visited = {origin}

    while len(queue):
        path = queue.pop(0)
        yield path

        node = path[-1]

        for neighb in adjacency_fn(node):
            newpath = path + [neighb]

            if neighb not in visited:
                visited.add(neighb)
                queue.append(newpath)

def adjacent_coords_cw(pos: tuple[int, int], side) -> tuple[int, int]:
    i, j = pos

    match side:
        case 0: return (i-1, j)
        case 1: return (i, j+1)
        case 2: return (i+1, j)
        case 3: return (i, j-1)
        case _: raise ValueError("Invalid orientation given.")