"""Pytest configuration: make the project root importable.

The chess engine modules (board.py, moves.py, ai.py) live one
directory up from tests/. Add the project root to sys.path so tests
can `from board import Board` without a package install.
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
