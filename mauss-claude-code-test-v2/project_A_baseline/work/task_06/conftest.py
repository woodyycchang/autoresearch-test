"""Pytest configuration: ensures the work dir is on sys.path."""

import os
import sys

# Make server.py / tokens.py / storage.py importable from tests/.
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
