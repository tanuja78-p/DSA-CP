from m2.min_heap import MinHeap


def test_min_heap():
    heap = MinHeap()

    print("=== MIN HEAP TEST ===")

    # Insert elements in unsorted order
    heap.insert(50, "Node-50")
    heap.insert(20, "Node-20")
    heap.insert(40, "Node-40")
    heap.insert(10, "Node-10")
    heap.insert(30, "Node-30")

    print("Heap size:", heap.size())
    print("Minimum element:", heap.peek())

    # Extract elements
    print("\nExtraction order:")

    while not heap.is_empty():
        print(heap.extract_min())

    print("\nHeap size after extraction:", heap.size())

    # Verify empty heap
    print("Heap empty:", heap.is_empty())


if __name__ == "__main__":
    test_min_heap()