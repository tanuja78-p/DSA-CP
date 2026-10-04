from typing import Any, Optional


class HashMap:
    """
    Simple HashMap implementation for M1.

    The HashMap provides fast lookup of information
    using a key.

    It will be used for:
        - Road lookup
        - Node lookup
        - Road status lookup
        - Hazard-related lookup

    This implementation uses separate chaining to
    handle hash collisions.
    """

    def __init__(
        self,
        capacity: int = 100003
    ):
        """
        Create an empty HashMap.

        capacity:
            Number of buckets used by the table.
        """

        self.capacity = capacity

        self.buckets = [
            []
            for _ in range(self.capacity)
        ]

        self.size = 0

    def _hash(
        self,
        key: Any
    ) -> int:
        """
        Convert a key into a bucket index.
        """

        return hash(key) % self.capacity

    def put(
        self,
        key: Any,
        value: Any
    ):
        """
        Insert or update a key-value pair.
        """

        index = self._hash(key)

        bucket = self.buckets[index]

        for item in bucket:

            if item[0] == key:

                item[1] = value

                return

        bucket.append(
            [key, value]
        )

        self.size += 1

    def get(
        self,
        key: Any,
        default: Optional[Any] = None
    ) -> Any:
        """
        Retrieve the value associated with a key.

        Returns default if the key does not exist.
        """

        index = self._hash(key)

        bucket = self.buckets[index]

        for item in bucket:

            if item[0] == key:
                return item[1]

        return default

    def contains(
        self,
        key: Any
    ) -> bool:
        """
        Check whether a key exists.
        """

        index = self._hash(key)

        bucket = self.buckets[index]

        for item in bucket:

            if item[0] == key:
                return True

        return False

    def remove(
        self,
        key: Any
    ) -> bool:
        """
        Remove a key-value pair.

        Returns:
            True if removed.
            False if the key did not exist.
        """

        index = self._hash(key)

        bucket = self.buckets[index]

        for position, item in enumerate(bucket):

            if item[0] == key:

                bucket.pop(position)

                self.size -= 1

                return True

        return False

    def keys(self):
        """
        Return all keys stored in the HashMap.
        """

        result = []

        for bucket in self.buckets:

            for item in bucket:

                result.append(item[0])

        return result

    def values(self):
        """
        Return all values stored in the HashMap.
        """

        result = []

        for bucket in self.buckets:

            for item in bucket:

                result.append(item[1])

        return result

    def items(self):
        """
        Return all key-value pairs.
        """

        result = []

        for bucket in self.buckets:

            for item in bucket:

                result.append(
                    (item[0], item[1])
                )

        return result

    def clear(self):
        """
        Remove all entries.
        """

        self.buckets = [
            []
            for _ in range(self.capacity)
        ]

        self.size = 0

    def __len__(self):
        """
        Return number of stored entries.
        """

        return self.size