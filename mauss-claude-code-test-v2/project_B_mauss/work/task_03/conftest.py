"""Pytest conftest -- add work dir to sys.path so tests can import lexer/parser/renderer."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
