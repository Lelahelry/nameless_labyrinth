# -*- coding: utf-8 -*-

from typing import Iterable, Callable, Iterator, TypeVar

T = TypeVar('T')

def pairwise(r: Iterable[T]) -> Iterator[tuple[T, T]]:
    """Iterates over an iterable pairwise, i.e. (0, 1), (1, 2), (2, 3), ...
    ----------
    Input: iterable
    Output: iterator of tuples"""
    it = iter(r)

    a = next(it)
    for b in it:
        yield (a, b)
        a = b

def bfs_walk(origin: T, adjacency_fn: Callable[[T], Iterable[T]]) -> Iterator[list[T]]:
    """Walks through a graph using breadth-first search.
    ----------
    Input: origin node, adjacency function
    Output: iterator of paths"""
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
    """Returns the coordinates of the tile adjacent to the given position on the given side.
    ----------
    Input: position (tuple[int,int]), side
    Output: adjacent position (tuple[int,int])"""
    i, j = pos

    match side:
        case 0: return (i-1, j)
        case 1: return (i, j+1)
        case 2: return (i+1, j)
        case 3: return (i, j-1)
        case _: raise ValueError("Invalid orientation given.")