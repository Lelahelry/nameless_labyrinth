from typing import Iterable, Callable

def pairwise(r: Iterable):
    it = iter(r)

    a = next(it)
    for b in it:
        yield (a, b)
        a = b

def bfs_walk(origin: tuple[int, int], adjacency_fn: Callable):
    queue = [origin]
    done = {origin}

    while len(queue):
        pos = queue.pop(0)
        yield pos

        for neighb in adjacency_fn(pos):
            if neighb not in done:
                done.add(neighb)
                queue.append(neighb)