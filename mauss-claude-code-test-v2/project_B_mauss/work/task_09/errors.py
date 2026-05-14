"""Validation error definitions for the form validator."""


class ValidationError:
    """Represents a single validation error with a path and message."""

    __slots__ = ("path", "message")

    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message

    def __repr__(self) -> str:
        return f"ValidationError(path={self.path!r}, message={self.message!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ValidationError):
            return NotImplemented
        return self.path == other.path and self.message == other.message

    def __hash__(self) -> int:
        return hash((self.path, self.message))

    def to_dict(self) -> dict:
        return {"path": self.path, "message": self.message}


class SchemaError(Exception):
    """Raised when a schema definition itself is invalid."""
    pass
