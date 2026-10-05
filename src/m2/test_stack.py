from m2.stack import Stack


def test_stack():
    stack = Stack()

    print("=== STACK TEST ===")

    stack.push("Node-1")
    stack.push("Node-2")
    stack.push("Node-3")
    stack.push("Node-4")

    print("Stack size:", stack.size())
    print("Top element:", stack.peek())

    print("\nExtraction order:")

    while not stack.is_empty():
        print(stack.pop())

    print("\nStack size after extraction:", stack.size())
    print("Stack empty:", stack.is_empty())


if __name__ == "__main__":
    test_stack()