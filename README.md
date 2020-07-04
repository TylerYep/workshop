# workshop

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Build Status](https://travis-ci.com/TylerYep/workshop.svg?branch=master)](https://travis-ci.com/TylerYep/workshop)
[![GitHub license](https://img.shields.io/github/license/TylerYep/workshop)](https://github.com/TylerYep/workshop/blob/master/LICENSE)

My design studio of AI/ML/CS concepts.

Separated into two sections:
- Algorithms + Data Structures
- AI/ML

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

# Goals
1. Readability. Everything should make it immediately obvious how the layer or mmodel works on its own.
2.


No autograd - if you want a simple autograd implementation, check out Karpathy's micrograd repo.

TODO:

- Convert to dataclasses?