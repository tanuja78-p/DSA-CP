class SortingUtils:
    """
    Custom sorting utilities for Member 3.

    Uses Merge Sort instead of Python's built-in sorted()
    so the DSA contribution is explicit and explainable.
    """

    @staticmethod
    def merge_sort(items, key):
        """
        Sort a list using Merge Sort.

        Parameters:
            items: list of dictionaries/objects
            key: function used to extract the value to sort by

        Returns:
            New sorted list.
        """

        if len(items) <= 1:
            return items.copy()

        middle = len(items) // 2

        left = SortingUtils.merge_sort(
            items[:middle],
            key
        )

        right = SortingUtils.merge_sort(
            items[middle:],
            key
        )

        return SortingUtils._merge(
            left,
            right,
            key
        )

    @staticmethod
    def _merge(left, right, key):
        """Merge two already sorted lists."""

        result = []

        i = 0
        j = 0

        while i < len(left) and j < len(right):

            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1

            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1

        while j < len(right):
            result.append(right[j])
            j += 1

        return result

    @staticmethod
    def sort_shelters(shelters):
        """
        Sort shelters by suitability score.

        Lower suitability score = better.
        """

        return SortingUtils.merge_sort(
            shelters,
            key=lambda shelter: shelter["score"]
        )

    @staticmethod
    def sort_routes(routes):
        """
        Sort routes by route cost.

        Lower route cost = better.
        """

        return SortingUtils.merge_sort(
            routes,
            key=lambda route: route["cost"]
        )

    @staticmethod
    def sort_destinations(destinations):
        """
        Sort evacuation destinations by priority.

        Lower priority number = higher priority.
        """

        return SortingUtils.merge_sort(
            destinations,
            key=lambda destination: destination["priority"]
        )