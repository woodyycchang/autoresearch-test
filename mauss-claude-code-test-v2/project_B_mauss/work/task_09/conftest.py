"""Pytest configuration: put the task_09 dir on sys.path so tests can import."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
