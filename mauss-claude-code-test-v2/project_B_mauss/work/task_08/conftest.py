"""Pytest config: ensure the regex package is importable from this dir."""

import sys
from pathlib import Path

# Add parent directory to sys.path so `import regex_engine` works.
HERE = Path(__file__).parent.resolve()
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
sys.path.insert(0, str(HERE))
