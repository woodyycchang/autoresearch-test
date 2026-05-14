# Handoff Note for Validator

## What was built

A Binary Search Tree (BST) class implemented in `solution.py` using only the Python standard library.

## Public API

The `BST` class exposes:
- `insert(value)` — inserts a value into the tree; duplicates are silently ignored.
- `delete(value)` — removes a value if present; no-op if absent (including on empty tree).
- `search(value)` — returns `True` if the value is in the tree, else `False`.
- `inorder()` — returns a list of all values in ascending sorted order.

## Implementation notes

- Internal `_Node` helper class with `value`, `left`, `right` slots.
- `insert` and `delete` are recursive; `search` is iterative.
- Deletion of a node with two children uses the inorder successor (min of right subtree).
- Values must be mutually comparable (works with ints, floats, strings, etc.).

## Files

- `solution.py` — implementation (one `BST` class plus a private `_Node`).
- `test_solution.py` — 17 pytest test cases covering empty tree, insertion (incl. duplicates), search hits/misses, deletion of leaves, single-child nodes, two-child nodes, the root, missing values, an empty tree, all-values deletion, randomized sorted-order check, string keys, and mixed operations.

## How to run tests

```
pytest test_solution.py -v
```

All tests pass.
