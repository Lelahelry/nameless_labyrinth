# Non-trivial function description

## Introduction, MVC

For the **algorithmically interesting function description**, we're going to take a deep dive through the code of the `GameController.validate_move` method.

In order to properly introduce this method, we'll first talk about the `GameController` class, which defines the object that will orchestrate game flow, provide interaction between the **User Interface** and the **Game State** and be the entrypoint of the application. This class posseses two main attributes:

- `model` of type `GameData`, which contains all of the game's data and state variables. It can be polled by the controller but rarely alters itself.
- `view` of type `GameView`, which holds and represents all user interface elements and interacts with the controller via conveniently defined methods.

As a technical fact, this design pattern is called a **Model-View-Controller architecture** and this game's code implements our approximate take on it.

All this talk is relevant to our explanation, first because it provides context on why we do things the way we do, and second because it now allows us to describe the calling context of our interesting method.

We can now say that the `validate_move` is called by the view upon the user clicking on a `Tile` on which they want to move their `Pawn` by way of an intermediate callback method tied to the `Board` canvas.

## Destructuring / Unpacking

Now, let's look at the code of our method:

```py
class GameController:
    ...
    
    def validate_move(self, newpos: tuple[int, int]) -> bool:
        pawn = self.model.get_active_player()
        startpos, _ = self.model.get_pawn_container(pawn)
        end_reached = False

        steps = []
        paths = (path for path in bfs_walk(startpos, self.model.get_adjacency_fn()) if not end_reached)
        for path in paths:

            endpos = path[-1]
            if endpos == newpos:
                end_reached = True
                steps = path

        self.next_path = steps
        return end_reached
```

First, we read the method's signature and see that it takes a pair of `int` (more commonly known as coordinates) as input and returns a `bool`. That, along with the method's name already gives us a lot of hints as to what this method does.

We then reach the start of this method's code, where we intitalize the variables that we will later need.

```py
pawn = self.model.get_active_player()
startpos, _ = self.model.get_pawn_container(pawn)
end_reached = False
...
```

Here, we first need to poll the model to obtain a reference to the actively playing `Pawn`. We then use this reference and again ask the model to find the tile that contains this `Pawn` and its own position in the overarching board. We won't explain here what these two model methods do, but you can probably imagine that their implementation is nothing too interesting.

Since the `get_pawn_container` method returns a 2-tuple, we use a **destructuring pattern** to assign its values to more meaningful variable names. The second member is a reference to the `Tile` object that contains the `Pawn`, but since we don't need it, we use an **underscore as variable name**, commonly called a **"discard pattern"**, to indicate to the interpreter or compiler that we won't use this variable and that it doesn't need to spend resources on properly initializing it. As a side note, destructuring patterns are one of the many places in the Python language where **iterators**, the stars of today's show, are implicitly used, but we'll properly introduce this concept in a few more lines.

Then we simply initialize another boolean variable that will enable us to optimize our code.

## Iterables, Iterators, Generators

Now, reaching the meat of the method.

```py
...
steps = []
paths = (path for path in bfs_walk(startpos, self.model.get_adjacency_fn()) if not end_reached)
for path in paths:

    endpos = path[-1]
    if endpos == newpos:
        end_reached = True
        steps = path
...
```

We first initialize the steps variable as an empty list since we need it define on every possible code path. From here, we finally need to understand the concepts of `Iterable`, `Iterator` and `Generator` as they are defined **in Python**.

1. An `Iterable[T]` object is an object which defines, for any type `T`, an `__iter__(self) -> Iterator[T]` method, such that you can call `iter(iterable)` on it and get an iterator.

2. An `Iterator[T]` object is a object implementing, for any type `T`, an `__iter__(self) -> Iterator[T]` method (usually returning itself) and a `__next__(self) -> T` method, such that you can also call `next(iterator)` on it to access its contents one-by-one.

3. A `Generator` function on `T` is a special kind of function that returns an `Iterator[T]` object and is defined using `yield` instead of `return` keywords, thus not returning anything in the traditional sense.

Per the previous definitions, we understand that **using generators gives us iterators**, that **iterators are iterables** and that **iterables can be, but are not always iterators**.

Examples of **common iterables are most sequence and container types**, such as `list`, `dict`, `tuple`, `set` and more. Examples of **common generator functions** are the `enumerate` and `zip` utilities. There are really no common examples of iterators as they are a common, unseen part of **Python**'s inner workings.

## For loops, examples

Now, we can understand what really happens when using a `for` loop. Let's review a few examples:

```py
# THIS
for element in things:
    do_something(element)

# Equivalent to

# THAT
it = iter(things)
loop = True
while loop:
    try:
        element = next(it)
        do_something(element)
    except StopIteration:
        loop = False
```

This is how `for` loops can be reimplmented using `while` loops in **Python**, and is actually about what it looks like under the hood. Destructuring/unpacking is used to assign the variables at each iteration, and the `__next__` method raises a `StopIteration` error upon having exhausted its **iterator**. This is actually how for loops know when to stop!

```py
def enumerate(iterable, start=0):
    it = iter(iterable)
    count = start

    for element in it:
        yield count, element
        count += 1

for index, element in enumerate(things):
    do_something()
```

Here is how a function such as `enumerate` can be implemented as **a generator, counting and yielding as it goes**. Again, unpacking is used to assign the variables and the `__iter__` method allows us to **generalize our function to any iterable object**.

In practice, it is preferable to use functions such as `enumerate` and `zip` with **iterable types and not their associated iterators**, because those will exhaust themselves and successive use could lead to unexpected behavior. In short, calling `iter` on iterables and then `next` on the resulting object will **generally guarantee the same behavior on repetition**, whereas calling `iter` on iterators and `next` repetitively will **deplenish them until empty then not work anymore**.

With all that, we can now understand the next line of our interesting method:

```py
...
paths = (path for path in bfs_walk(startpos, self.model.get_adjacency_fn()) if not end_reached)
...
```

Here, we use **generator comprehension** syntax to create a generator from another generator. We simply arrange the elements as they are given by `bfs_walk`, only adding a confition for passing the elements at the end. What needs to be known here is that conditinal expressions are **lazy evaluated** in generator expressions. This means that the condition will actually be inspected by the interpreter **only when it actually needs to access each element** (i.e., when `__next__` is called), and **not at instanciation time** like if we had used a list comprehension. This allows us to **dynamically adjust the iterator by updating the condition**.

## BFS, adjacency function

By now, you may have guessed that `bfs_walk` is another generator that yields elements in BFS order, and you'd be almost right! Let's take a look at its definition:

```py
def bfs_walk(origin: T, adjacency_fn: Callable[[T], Iterable[T]]) -> Iterator[list[T]]:
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
```

This looks very much like a standard BFS implementation, only **there's no stopping or return condition**, it traverses the graph until the end since we want to iterate on the graph. A few bits are also modified in order to remember and yield the paths instead of the nodes. Primarily, we have `adjacency_fn` as a parameter, so that the graph does not have to be strictly specified, but only needs to provide an adjacency function that returns, for any given **node**, an **iterator over its neigboring nodes**

Back to our concrete example, we see that `bfs_walk` is called with the `GameData.get_adjacency_fn` method which returns the `Board.connected_tiles` generator function. Looking at it:

```py
class Board:
    ...

    def connected_tiles(self, origin_pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        origin = self.grid[origin_pos]
        for idx, side in enumerate(origin.sides):
            if side:
                idx = (origin.orientation + idx)%4
                neighb_pos = adjacent_coords_cw(origin_pos, idx)
                neighb = self.grid.get(neighb_pos)
                if neighb is None: continue

                opp = (-neighb.orientation + idx + 2)%4
                if not neighb.sides[opp]: continue
                
                yield neighb_pos
```

We see that this `Board` method takes the origin coordinates as input, computes the origin's adjacencies with that of its neighbors, and then yields the connected neighbors' positions.

Now, we understand that **paths is an iterator over the possible paths that the current player can take**, starting from its own position.

## Method end

Finally, we can take a look at the rest of the method:

```py
...
for path in paths:

    endpos = path[-1]
    if endpos == newpos:
        end_reached = True
        steps = path

self.next_path = steps
return end_reached
```

Iterating over the BFS paths in BFS order, we are confident that **we will reach our objective if it is possible to do so**. We check if we reach our desired position and if so, update the condition and the steps list. Thanks to lazy evaluation, changing `end_reached` to `True` allows us to **stop iterating uselessly as soon as possible** (all while avoid the use of `break` keywords and `while` loops).

We finally record the path so that the controller can remember it and return the validity of the move to the caller.

## Conclusion

This marks the end of the `validate_move` algorithmic description. To sum up, you now should grasp the concepts of MVC design patterns, destructuring/unpacking, Iterables/Iterators/Generators, For-loop internals and BFS!

Thanks for reading us, we hope you liked this :)
