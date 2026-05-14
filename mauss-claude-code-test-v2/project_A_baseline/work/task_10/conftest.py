"""pytest config: ensure the work directory is importable for tests."""
import os
import sys

# Make model.py / generator.py / storage.py importable from tests/
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
