from typing import Iterable, Callable, Iterator, TypeVar

T = TypeVar('T')

def pairwise(r: Iterable[T]) -> Iterator[tuple[T, T]]:
    it = iter(r)

    a = next(it)
    for b in it:
        yield (a, b)
        a = b

def bfs_walk(origin: T, adjacency_fn: Callable[[T], Iterator[T]]) -> Iterator[T]:
    queue = [origin]
    done = {origin}

    while len(queue):
        node = queue.pop(0)
        yield node

        for neighb in adjacency_fn(node):
            if neighb not in done:
                done.add(neighb)
                queue.append(neighb)

def adjacent_coords_cw(pos: tuple[int, int], side) -> tuple[int, int]:
    i, j = pos

    match side:
        case 0: return (i-1, j)
        case 1: return (i, j+1)
        case 2: return (i+1, j)
        case 3: return (i, j-1)
        case _: raise ValueError("Invalid orientation given.")