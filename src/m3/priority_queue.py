class PriorityQueueItem:
    def __init__(self, priority, shelter, details=None):
        self.priority = priority
        self.shelter = shelter
        self.details = details or {}


class ShelterPriorityQueue:
    """
    Custom binary min-heap.

    Lowest suitability score gets highest priority.
    """

    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def _parent(self, index):
        return (index - 1) // 2

    def _left(self, index):
        return 2 * index + 1

    def _right(self, index):
        return 2 * index + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = (
            self.heap[j],
            self.heap[i],
        )

    def push(self, priority, shelter, details=None):
        """Insert shelter into priority queue."""
        item = PriorityQueueItem(
            priority,
            shelter,
            details,
        )

        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        while index > 0:

            parent = self._parent(index)

            if self.heap[parent].priority <= self.heap[index].priority:
                break

            self._swap(parent, index)
            index = parent

    def pop(self):
        """Remove and return highest-priority shelter."""
        if self.is_empty():
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        top = self.heap[0]

        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return top

    def _heapify_down(self, index):
        while True:

            left = self._left(index)
            right = self._right(index)

            smallest = index

            if (
                left < len(self.heap)
                and self.heap[left].priority
                < self.heap[smallest].priority
            ):
                smallest = left

            if (
                right < len(self.heap)
                and self.heap[right].priority
                < self.heap[smallest].priority
            ):
                smallest = right

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest

    def peek(self):
        """Return best shelter without removing it."""
        if self.is_empty():
            return None

        return self.heap[0]

    def clear(self):
        self.heap.clear()