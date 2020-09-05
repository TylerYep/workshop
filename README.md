# workshop

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
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

## TODO List

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
