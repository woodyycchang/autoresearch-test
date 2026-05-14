"""Binary Search Tree implementation.

Supports insert, delete, search, and inorder traversal.
No duplicates allowed (insert of an existing value is a no-op).
"""

from __future__ import annotations
from typing import Any, List, Optional


class _Node:
    """Internal BST node holding a value and left/right child references."""

    __slots__ = ("value", "left", "right")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.left: Optional[_Node] = None
        self.right: Optional[_Node] = None


class BinarySearchTree:
    """A simple (unbalanced) Binary Search Tree.

    Values must be mutually comparable via ``<`` and ``>``. Duplicates are
    silently ignored on ``insert``.
    """

    def __init__(self) -> None:
        self._root: Optional[_Node] = None
        self._size: int = 0

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def insert(self, value: Any) -> None:
        """Insert ``value`` into the tree. No-op if already present."""
        self._root, inserted = self._insert(self._root, value)
        if inserted:
            self._size += 1

    def delete(self, value: Any) -> None:
        """Delete ``value`` from the tree if present; no-op otherwise."""
        self._root, deleted = self._delete(self._root, value)
        if deleted:
            self._size -= 1

    def search(self, value: Any) -> bool:
        """Return True iff ``value`` exists in the tree."""
        node = self._root
        while node is not None:
            if value == node.value:
                return True
            if value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def inorder(self) -> List[Any]:
        """Return values in ascending (sorted) order via inorder traversal."""
        result: List[Any] = []
        self._inorder(self._root, result)
        return result

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: Any) -> bool:
        return self.search(value)

    # ------------------------------------------------------------------ #
    # Internal helpers (recursive)
    # ------------------------------------------------------------------ #
    def _insert(self, node: Optional[_Node], value: Any) -> tuple:
        if node is None:
            return _Node(value), True
        if value == node.value:
            # No duplicates.
            return node, False
        if value < node.value:
            node.left, inserted = self._insert(node.left, value)
        else:
            node.right, inserted = self._insert(node.right, value)
        return node, inserted

    def _delete(self, node: Optional[_Node], value: Any) -> tuple:
        if node is None:
            return None, False
        if value < node.value:
            node.left, deleted = self._delete(node.left, value)
            return node, deleted
        if value > node.value:
            node.right, deleted = self._delete(node.right, value)
            return node, deleted

        # Found node to delete.
        if node.left is None and node.right is None:
            return None, True
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        # Two children: replace value with inorder successor (smallest in
        # right subtree), then delete that successor from the right subtree.
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.value = successor.value
        node.right, _ = self._delete(node.right, successor.value)
        return node, True

    def _inorder(self, node: Optional[_Node], out: List[Any]) -> None:
        if node is None:
            return
        self._inorder(node.left, out)
        out.append(node.value)
        self._inorder(node.right, out)
