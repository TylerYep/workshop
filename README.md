# workshop

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Build Status](https://travis-ci.com/TylerYep/workshop.svg?branch=master)](https://travis-ci.com/TylerYep/workshop)
[![GitHub license](https://img.shields.io/github/license/TylerYep/workshop)](https://github.com/TylerYep/workshop/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/TylerYep/workshop/branch/master/graph/badge.svg)](https://codecov.io/gh/TylerYep/workshop)
[![Downloads](https://pepy.tech/badge/csworkshop)](https://pepy.tech/project/csworkshop)

My design studio of AI/ML/CS concepts. Code is adapted from many different websites across the Internet.

Separated into three sections:

- Algorithms
- Math
- Data Structures

# Usage

```
pip install csworkshop
```

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
