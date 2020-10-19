# workshop

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Build Status](https://travis-ci.com/TylerYep/workshop.svg?branch=master)](https://travis-ci.com/TylerYep/workshop)
[![GitHub license](https://img.shields.io/github/license/TylerYep/workshop)](https://github.com/TylerYep/workshop/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/TylerYep/workshop/branch/master/graph/badge.svg)](https://codecov.io/gh/TylerYep/workshop)

My design studio of AI/ML/CS concepts.

Separated into two sections:

- Algorithms + Data Structures
- AI/ML

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
Benefits:

- `__init__`, in constructors that simply set all parameters.
- `__eq__`, which ensures that a tuple of object fields are compared.
- `__repr__`, which is perfect for error messages. We want to prettify output when used as a string, but use the dataclass default repr in all other cases, e.g. error messages.
- `@dataclass(order=True)` when nodes or structs should be comparable. If a dataclass is not ideal, using `@functools.total_ordering` is a viable alternative.

My choices:

- Explicitly define the `__init__` function whenever you have more initialization logic than "set all parameters as fields". A common example is when a self member variable shouldn't be a constructor parameter. This makes reading the class much easier and allows better control over the logic.
- Create a separate `__str__` function to use when printing the object for visualizing the state of the data structure. `__repr__` should contain a single line while string should be pretty printed.
- Define `__hash__` myself, since I can choose the necessary fields to make a unique hash. Additionally, using `@dataclass(frozen=True)` is almost never a good idea, since you won't be able to even set attributes in `__post_init__`, and the docs specifically point out a performance penalty.
- Prefer the `@dataslots` and the _dataslots_ library over using `__slots__`. It is a clean single decorator and dependency rather than an ugly list of strings.

# Style Guide

## Pre-Commit
- I use local installations of pre-commit configs because most of the time I work on projects on my own. If a project becomes big enough to warrant more collaborators, then we should use the GitHub URL of the hook. We might eventually want to move to the github versions if we add pre-commit to CI, using --all.
- All type checking and linting should only happen on changed files, assuming a clean run to begin with.
- We include pytest because it's more annoying to look at CI breaking than to wait a bit and fix it to begin with.
- Pytest should always run on all files, since we expect those to be only the unit tests, and as a result, very fast.
- If we limit pytest to changed files, then it runs on all files only when there are no changed files,
and runs on only a couple files if many files are changed. Not what we want, I think.

- Order functions within a class using flake8-function-order.

- Iterables cannot be indexed and must get length by casting to tuple or set.
- Sequences can be indexed.

### Types and Data Structures

Associative Arrays
Unrolled Linked List
Bloom Filter
Cuckoo Filter
Merkle Tree
Treaps
Fenwick Tree
AVL Tree
Scapegoat Tree
Splay Tree
Binomial Heap
Pairing Heap
Spanning Trees
Social Networks
Strings

# Algorithms

Backpack Problem
Egg Dropping
Fast Fibonacci Transform
A\* Search
Johnson's Algorithm
Matching (Graph Theory)
Matching Algorithms (Graph Theory)
Flow Network
Max-flow Min-cut Algorithm
Ford-Fulkerson Algorithm
Edmonds-Karp Algorithm
Shunting Yard Algorithm
Rabin-Karp Algorithm
Basic Shapes, Polygons, Trigonometry
Convex Hull
Grids
Finite State Machines
Turing Machines
Halting Problem
Kolmogorov Complexity
Traveling Salesperson Problem
Pushdown Automata
Regular Languages
Context Free Grammars
Context Free Languages
Signals and Systems
Linear Time Invariant Systems
Predicting System Behavior

# Cryptography and Simulations

Caesar Cipher
Vigenère Cipher
RSA Encryption
Enigma Machine
Diffie-Hellman
Knapsack Cryptosystem
Secure Hash Algorithms
Entropy (Information Theory)
Error correcting codes
Symmetric Ciphers
Inverse Transform Sampling
Monte-Carlo Simulation
Annealing
Genetic Algorithms

# Machine Learning

Feature Vector
Naive Bayes Classifier
Perceptron
Principal Component Analysis
Ridge Regression
k-Means Clustering
Markov Chains
Hidden Markov Models
Gaussian Mixture Model
Collaborative Filtering
Artificial Neural Network

- Name BFS, DFS after their functionality rather than the algorithm name.
- The title belongs in the import?
- Kargers, Kruskals, etc

from src.algorithms import kargers
kargers.partition_graph()

from src.algorithms.kargers import partition_graph
partition_graph()

from src.algorithms import kargers
kargers()

from src.algorithms import breadth_first_search
breadth_first_search()

from src.algorithms import bfs
bfs.find_path()

from src.algorithms.bfs import find_path
find_path()

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
