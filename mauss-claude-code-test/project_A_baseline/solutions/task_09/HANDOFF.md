# Task 09 Handoff

## What was built

`solution.py` implements:

- `ListNode` class with `val` and `next` attributes (uses `__slots__`).
- `has_cycle(head)` function using Floyd's tortoise-and-hare algorithm.
  - O(n) time, O(1) extra space.
  - Two pointers advance at speeds 1 and 2; they meet iff a cycle exists.
  - Returns `False` for `None` / empty list.
- `build_list(values, cycle_index=-1)` helper to construct test lists.
  - When `0 <= cycle_index < len(values)`, the tail's `next` points back to
    `nodes[cycle_index]`, creating a cycle.
  - Otherwise the list is acyclic.

## How to run

```bash
cd <this directory>
pytest test_solution.py -v
```

## Test coverage

`test_solution.py` covers:

- Empty list, single node (with and without self-cycle).
- Acyclic lists (short and long, 100 nodes).
- Cycles at head, middle, and tail positions.
- Long cycle (1000 nodes, cycle_index=500).
- `build_list` helper correctness, including invalid `cycle_index` values.
- `ListNode` default construction and explicit `val`/`next`.
- Returns `bool` (not truthy/falsy other types).

## Notes for Validator

- Stdlib + pytest only (no third-party deps).
- No `output.txt` is produced.
- File layout: `solution.py`, `test_solution.py`, `HANDOFF.md`.
