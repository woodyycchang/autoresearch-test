"""Pytest config: ensure the work dir is on sys.path so tests can import the
lexer/parser/renderer modules directly."""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
