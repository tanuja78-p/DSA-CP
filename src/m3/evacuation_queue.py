from collections import deque


class EvacuationQueue:
    """
    Queue for processing evacuation groups.

    Flow:
        WAITING -> ON_ROUTE -> ARRIVED
    """

    def __init__(self):
        self._queue = deque()

    def enqueue(self, evacuee_group):
        """Add an evacuation group to the queue."""
        evacuee_group.status = "WAITING"
        self._queue.append(evacuee_group)

    def dequeue(self):
        """Remove and return the next evacuation group."""
        if not self._queue:
            return None

        group = self._queue.popleft()
        group.status = "ON_ROUTE"
        return group

    def peek(self):
        """Return the next group without removing it."""
        if not self._queue:
            return None

        return self._queue[0]

    def mark_arrived(self, evacuee_group):
        """Mark an evacuation group as arrived."""
        evacuee_group.status = "ARRIVED"

    def is_empty(self):
        """Return True if the queue is empty."""
        return len(self._queue) == 0

    def size(self):
        """Return the number of groups waiting in the queue."""
        return len(self._queue)

    def clear(self):
        """Remove all groups from the queue."""
        self._queue.clear()

    def get_all(self):
        """Return all currently waiting groups."""
        return list(self._queue)