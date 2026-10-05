class Stack:
    """
    Stack data structure for route reconstruction.

    Follows LIFO:
    Last In, First Out.
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek into an empty stack.")
        return self.items[-1]