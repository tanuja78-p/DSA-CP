class MinHeap:
    """
    Min Heap priority queue for Member 2 routing algorithms.

    Each heap entry is stored as:
        (priority, node_id)

    The entry with the smallest priority is always
    available at the root of the heap.
    """

    def __init__(self):
        self.heap = []

    def is_empty(self):
        """Return True if the heap contains no elements."""
        return len(self.heap) == 0

    def size(self):
        """Return the number of elements in the heap."""
        return len(self.heap)

    def insert(self, priority, node_id):
        """
        Insert a new (priority, node_id) entry
        and restore the Min Heap property.
        """

        self.heap.append((priority, node_id))

        index = len(self.heap) - 1

        while index > 0:
            parent = (index - 1) // 2

            if self.heap[parent][0] <= self.heap[index][0]:
                break

            self.heap[parent], self.heap[index] = (
                self.heap[index],
                self.heap[parent]
            )

            index = parent

    def extract_min(self):
        """
        Remove and return the entry with the smallest priority.

        Returns:
            (priority, node_id)

        Raises:
            IndexError if the heap is empty.
        """

        if self.is_empty():
            raise IndexError("Cannot extract from an empty heap.")

        if len(self.heap) == 1:
            return self.heap.pop()

        minimum = self.heap[0]

        self.heap[0] = self.heap.pop()

        index = 0
        size = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if (
                left < size
                and self.heap[left][0] < self.heap[smallest][0]
            ):
                smallest = left

            if (
                right < size
                and self.heap[right][0] < self.heap[smallest][0]
            ):
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = (
                self.heap[smallest],
                self.heap[index]
            )

            index = smallest

        return minimum

    def peek(self):
        """
        Return the smallest entry without removing it.

        Raises:
            IndexError if the heap is empty.
        """

        if self.is_empty():
            raise IndexError("Cannot peek into an empty heap.")

        return self.heap[0]