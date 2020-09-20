# workshop

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Build Status](https://travis-ci.com/TylerYep/workshop.svg?branch=master)](https://travis-ci.com/TylerYep/workshop)
[![GitHub license](https://img.shields.io/github/license/TylerYep/workshop)](https://github.com/TylerYep/workshop/blob/master/LICENSE)

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
Three packages are exposed to the user - algorithms, ml, and structures.
Imports are done quickly and painlessly. We avoid circular imports by importing algorithms needed to create data structures inline.

## Dataclasses
Dataclasses are one of the trickiest things to work with in Python. I tentatively have decided to make any class that would benefit from one of the below points into a dataclass.
Benefits:
- `__init__`, in constructors that simply set all parameters.
- `__eq__`, which ensures that a tuple of object fields are compared.
- `__repr__`, which is perfect for error messages.
- `@dataclass(order=True)` when nodes or structs should be comparable. If a dataclass is not ideal, using `@functools.total_ordering` is a viable alternative.

My choices:
- Explicitly define the `__init__` function whenever you have more initialization logic than "set all parameters as fields". A common example is when a self member variable shouldn't be a constructor parameter. This makes reading the class much easier and allows better control over the logic.
- Create a separate `__str__` function to use when printing the object for visualizing the state of the data structure. `__repr__` should contain a single line while string should be pretty printed.
- Define `__hash__` myself, since I can choose the necessary fields to make a unique hash. Additionally, using `@dataclass(frozen=True)` is almost never a good idea, since you won't be able to even set attributes in `__post_init__`, and the docs specifically point out a performance penalty.
- Prefer the `@with_slots` and the _dataslots_ library over using `__slots__`. It is a clean single decorator and dependency rather than an ugly list of strings.

# Style Guide
- Use `scripts/install-hooks` to enforce all styles.
- Order functions within a class in the following order:





### Types and Data Structures
Double Ended Queues
Associative Arrays
Disjoint-set Data Structure (Union-Find)
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
Fibonacci Heap
Pairing Heap
Spanning Trees
Social Networks
Kruskal's Algorithm
Strings

# Algorithms
Backpack Problem
Egg Dropping
Fast Fibonacci Transform
Karatsuba Algorithm
A* Search
Bellman-Ford Algorithm
Floyd-Warshall Algorithm
Johnson's Algorithm
Matching (Graph Theory)
Matching Algorithms (Graph Theory)
Flow Network
Max-flow Min-cut Algorithm
Ford-Fulkerson Algorithm
Edmonds-Karp Algorithm
Shunting Yard Algorithm
Rabin-Karp Algorithm
Knuth-Morris-Pratt Algorithm
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
Huffman Code
Error correcting codes
Symmetric Ciphers
Inverse Transform Sampling
Monte-Carlo Simulation
Annealing
Genetic Algorithms
Programming Blackjack

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
