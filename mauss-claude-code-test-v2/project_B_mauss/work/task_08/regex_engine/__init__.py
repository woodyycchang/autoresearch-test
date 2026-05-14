"""NFA-based regex engine.

Public API:
    compile(pattern) -> Regex with .match / .search / .findall
"""

from .matcher import compile, Regex, SimulationLimitExceeded  # noqa: F401
from .compiler import ParseError  # noqa: F401

__all__ = ["compile", "Regex", "ParseError", "SimulationLimitExceeded"]
