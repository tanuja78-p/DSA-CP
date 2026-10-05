from m2.route_utils import reconstruct_path


def test_reconstruct_path():

    print("=== ROUTE RECONSTRUCTION TEST ===")

    parent = {
        "Node-2": "Node-1",
        "Node-3": "Node-2",
        "Node-4": "Node-3",
        "Node-5": "Node-4"
    }

    source = "Node-1"
    destination = "Node-5"

    path = reconstruct_path(parent, source, destination)

    print("Source:", source)
    print("Destination:", destination)
    print("Reconstructed path:", " -> ".join(path))

    print("\nPath length:", len(path))

    unreachable = reconstruct_path(
        parent,
        "Node-1",
        "Node-99"
    )

    print("Unreachable path:", unreachable)


if __name__ == "__main__":
    test_reconstruct_path()