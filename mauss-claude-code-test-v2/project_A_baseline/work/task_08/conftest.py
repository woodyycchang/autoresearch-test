"""Make the work directory importable for the test suite."""

import os
import sys

# Ensure the work directory (parent of `tests/`) is on sys.path so the test
# modules can `import matcher` etc.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
