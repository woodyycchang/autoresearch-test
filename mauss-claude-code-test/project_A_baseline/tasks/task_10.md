# Task 10

## Description

Implement a basic Markov chain text generator. Class `MarkovChain(order=1)`:
- `train(text)` — split text on whitespace, build transition table of order
  `order` (i.e. predict next word from the previous `order` words).
- `generate(length, seed=None)` — return a generated string of `length` words.
  If `seed` is provided, use it for deterministic output (so tests can pass).
  If the chain hits a dead end, restart from a random starting state from
  the training data.

## Your job

Build this. Write Python code AND unit tests. Run the tests and confirm they pass.

When done, write a 1-line summary of what you built to `output.txt`.
