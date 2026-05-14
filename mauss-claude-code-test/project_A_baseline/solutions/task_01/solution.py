"""Binary Search Tree implementation.

Supports insert, delete, search, and inorder traversal.
No duplicate values are stored.
"""


class _Node:
    __slots__ = ("value", "left", "right")

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    """A binary search tree that does not store duplicate values."""

    def __init__(self):
        self._root = None

    def insert(self, value):
        """Insert ``value`` into the tree. Duplicates are ignored."""
        self._root = self._insert(self._root, value)

    def _insert(self, node, value):
        if node is None:
            return _Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        # equal value: ignore (no duplicates)
        return node

    def search(self, value):
        """Return True if ``value`` is in the tree, else False."""
        node = self._root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def delete(self, value):
        """Delete ``value`` from the tree if present. No-op otherwise."""
        self._root = self._delete(self._root, value)

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Found the node to delete.
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Two children: replace with inorder successor (min of right subtree).
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return node

    def inorder(self):
        """Return a list of all values in sorted (ascending) order."""
        result = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node, out):
        if node is None:
            return
        self._inorder(node.left, out)
        out.append(node.value)
        self._inorder(node.right, out)
