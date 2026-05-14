"""Pytest configuration for task_04.

Adds the work-dir to sys.path so `import pipeline` works from tests/.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
