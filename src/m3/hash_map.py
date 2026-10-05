class HashMapEntry:
    """One entry inside the custom hash table."""

    def __init__(self, key, value):
        self.key = key
        self.value = value


class ShelterHashMap:
    """
    Custom HashMap for:

        shelter_id -> Shelter

    Collision handling:
        Separate chaining.
    """

    def __init__(self, capacity=17):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, key):
        """Generate bucket index."""
        return hash(str(key)) % self.capacity

    def put(self, key, value):
        """Insert or update a key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for entry in bucket:
            if entry.key == key:
                entry.value = value
                return

        bucket.append(HashMapEntry(key, value))
        self.size += 1

    def get(self, key, default=None):
        """Retrieve value by key."""
        index = self._hash(key)

        for entry in self.buckets[index]:
            if entry.key == key:
                return entry.value

        return default

    def contains(self, key):
        """Check whether key exists."""
        return self.get(key) is not None

    def remove(self, key):
        """Remove key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, entry in enumerate(bucket):
            if entry.key == key:
                bucket.pop(i)
                self.size -= 1
                return entry.value

        return None

    def values(self):
        """Return all stored values."""
        result = []

        for bucket in self.buckets:
            for entry in bucket:
                result.append(entry.value)

        return result

    def keys(self):
        """Return all keys."""
        result = []

        for bucket in self.buckets:
            for entry in bucket:
                result.append(entry.key)

        return result

    def __len__(self):
        return self.size