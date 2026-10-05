class BSTNode:
    """
    BST node.

    Multiple shelters can have the same available capacity,
    so each node stores a list of shelters.
    """

    def __init__(self, key, shelter):
        self.key = key
        self.shelters = [shelter]

        self.left = None
        self.right = None


class ShelterBST:
    """
    Binary Search Tree ordered by available shelter capacity.

    Smaller available capacity:
        left

    Larger available capacity:
        right
    """

    def __init__(self):
        self.root = None

    def insert(self, shelter):
        """Insert shelter based on available capacity."""
        key = shelter.available_capacity

        if self.root is None:
            self.root = BSTNode(key, shelter)
            return

        self._insert(self.root, key, shelter)

    def _insert(self, node, key, shelter):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, shelter)
            else:
                self._insert(node.left, key, shelter)

        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, shelter)
            else:
                self._insert(node.right, key, shelter)

        else:
            node.shelters.append(shelter)

    def inorder(self):
        """
        Return shelters in ascending order of available capacity.
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return

        self._inorder(node.left, result)

        for shelter in node.shelters:
            result.append(shelter)

        self._inorder(node.right, result)

    def reverse_inorder(self):
        """
        Return shelters in descending order of available capacity.
        """
        result = []
        self._reverse_inorder(self.root, result)
        return result

    def _reverse_inorder(self, node, result):
        if node is None:
            return

        self._reverse_inorder(node.right, result)

        for shelter in node.shelters:
            result.append(shelter)

        self._reverse_inorder(node.left, result)

    def search_capacity(self, capacity):
        """Find shelters with exact available capacity."""
        node = self.root

        while node is not None:

            if capacity == node.key:
                return list(node.shelters)

            if capacity < node.key:
                node = node.left
            else:
                node = node.right

        return []

    def clear(self):
        """Clear the tree."""
        self.root = None