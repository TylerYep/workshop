# workshop

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Build Status](https://travis-ci.com/TylerYep/workshop.svg?branch=master)](https://travis-ci.com/TylerYep/workshop)
[![GitHub license](https://img.shields.io/github/license/TylerYep/workshop)](https://github.com/TylerYep/workshop/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/TylerYep/workshop/branch/master/graph/badge.svg)](https://codecov.io/gh/TylerYep/workshop)
[![Downloads](https://pepy.tech/badge/csworkshop)](https://pepy.tech/project/csworkshop)

My design studio of AI/ML/CS concepts. Code is adapted from many different websites across the Internet.

Separated into three sections:

- Algorithms
- Math (AI/ML)
- Data Structures

# Usage

`pip install csworkshop`

```python
from cs.algorithms import binary_search
from cs.structures import Graph, FibonacciHeap
```

## Key Tenets

- Must work functionally
  - Unit tested, applicable
- Must be easy to read
  - Type-checkable, linted, and formatted code
  - Educational, designed for a CS students
  - Sacrifice efficiency and concision for readability

# Design Decisions

- Four packages are exposed to the user - algorithms, maths, ml, and structures.
- Imports are done quickly and painlessly. We avoid circular imports by importing algorithms needed to create data structures inline.
- The `__init__.py` file for the package contains all reasonable user-facing APIs. Tests use the imports from this file where possible, and in all other cases directly imports the function to test.

## Dataclasses

Dataclasses are one of the trickiest things to work with in Python. I tentatively have decided to make any class that would benefit from one of the below points into a dataclass.

If you want slots, and not using **post_init**, inherit NamedTuple.
If you have a dataclass, use @dataslots.

### Benefits

- `__init__`, in constructors that simply set all parameters.
- `__eq__`, which ensures that a tuple of object fields are compared.
- `__repr__`, which is perfect for error messages. We want to prettify output when used as a string, but use the dataclass default repr in all other cases, e.g. error messages.
- `@dataclass(order=True)` when nodes or structs should be comparable. If a dataclass is not ideal, using `@functools.total_ordering` is a viable alternative.

### My choices

- `@dataclass(init=False, eq=False, order=False, repr=False)` means don't use dataclasses.
- Explicitly define the `__init__` function whenever you have more initialization logic than "set all parameters as fields". A common example is when a self member variable shouldn't be a constructor parameter. This makes reading the class much easier and allows better control over the logic. Avoid **post_init** when possible.
- Create a separate `__str__` function to use when printing the object for visualizing the state of the data structure. `__repr__` should contain a single line while string should be pretty printed.
- Define `__hash__` myself, since I can choose the necessary fields to make a unique hash. Additionally, using `@dataclass(frozen=True)` is almost never a good idea, since you won't be able to even set attributes in `__post_init__`, and the docs specifically point out a performance penalty.
- Prefer the `@dataslots` and the _dataslots_ library over using `__slots__` all the time. It is a clean single decorator and dependency rather than an ugly list of strings.

# Style Guide

- Order functions within a class using flake8-function-order.
- Iterables cannot be indexed and must get length by casting to tuple or set. Sequences are indexable.
- Put test cases into classes to avoid naming conflicts!
- Name functions to include their algorithm name but also the purpose:

1. The best option - name includes classic algorithm name, as well as purpose.
   ```
   from cs.algorithms import breadth_first_search, kargers
   kargers_min_cut()
   breadth_first_search()
   ```
2. No point in making a class for each function.

   ```
   from cs.algorithms import bfs, kargers
   bfs.find_shortest_path()
   kargers.partition_graph()
   ```

3. Easier to import from overall algorithms, but what if we want to use two different algorithms for the same task?
   ```
   from cs.algorithms.bfs import find_shortest_path
   from cs.algorithms.kargers import partition_graph
   find_shortest_path()
   partition_graph()
   ```

## In-place operations vs Functional Paradigms in Python

- Avoid destructive operations in Python whenever possible.

```
h1.merge(h2)
h1 |= h2
BinomialHeap.merge(h1, h2)

h3 = h1.merge(h2)
h3 = h1 | h2
h3 = BinomialHeap.merge(h1, h2)
```

- Python has imperative paradigm when it comes to performing actions. For example, `stack.push(5)` does not return a new Stack. This is because we are not interested in keeping track of our state over time. Thus, it is an action that operates in place.

## Naming data structure methods

### Adding

- add - easily confused with arithmetic, but useful for stuff like sets, which can only increase.
- append - adds to end.
- push - adds to end or pile, like a stack.
- enqueue - encodes idea of inserting in one end and removing at a later time.
- insert - in my opinion should be able to specify index.

## Removing

- subtract - rarely ever used.
- dequeue - only used with enqueue.
- pop - remove but also return result.
- remove - gets rid of it in place.
- delete - clear memory in some way.
- banish - irreversible destruction.

## Pre-Commit

- I use local installations of pre-commit configs because most of the time I work on projects on my own. If a project becomes big enough to warrant more collaborators, then we should use the GitHub URL of the hook. We might eventually want to move to the github versions if we add pre-commit to CI, using --all.
- All type checking and linting should only happen on changed files, assuming a clean run to begin with.
- We include pytest because it's more annoying to look at CI breaking than to wait a bit and fix it to begin with.
- Pytest should always run on all files, since we expect those to be only the unit tests, and as a result, very fast.
- If we limit pytest to changed files, then it runs on all files only when there are no changed files,
  and runs on only a couple files if many files are changed. Not what we want, I think.

# Dynamic Shape-Checking / Type-Checking (Typorch)

I'm interested in shape-checking for tensors. It doesnt need to be static type checking,
having fancy asserts would be good enough.

> (B, C, H, W)

> (B, 1, H, W)

> (B, H, W)

If you run a program with the shape-checker, it automatically inserts assert statements that the left side of the variable assignment must have that shape. Letters are tracked throughout (e.g. a new letter introduces a new variable), and a number asserts that that dimension must match exactly.

Tuple shapes maybe, to distinguish a shape comment from a regular comment.

Using this mode, the code is compiled uniquely and increases runtime.

Once you are confident with your shapes, you can simply run your program normally.

# Line lengths

i am interested in arguing for an optimal python line length. PEP8 says 79 and black says 88, some people use 100 or 120.
What if the best answer is 90?

all were chosen pretty arbitrarily, but it shouldn't be hard to define a clever readability metric and choose optimal value based off that.

apparently the 88 comes from a study that compares 88 to 79 and found that 88 produces significantly shorter files, which is essentially reading compression (don't have to scroll as much). Let's try to prove/verify this result.

like plot runs of black -l N vs length of output file
and then take the max dual constraint thingy
like just treat it as an optimization problem, and we should get a better range than "somewhere from 79 -120"
the challenge being the data heavily skews to existing line length rules like PEP8 (familiarity bias)
at some point you want to cut off the tail of the distribution

and that way the code minimizes both height and width (multiply them together)

I need a stable version of Black and a way to remove all trailing commas to reset it.

To merge TheAlgorithms:

```fish
git pull upstream master
git rebase --abort
git merge upstream/master --strategy-option theirs
yes d | git mergetool --
```

# Python Upgrades

## 3.10

- Remove all `from __future__` imports.
  However, this might be painful if I need numpy, as I would need to add them all back.
- Add `zip(..., strict=True)` once mypy detects the new parameter.
- Remove all Optional[] type annotations in favor of int | None.
