from .base import StepLogger


def quick_sort(array: list[int]) -> list[dict]:
    """Lomuto-partition quick sort.

    Pick the last element as pivot, partition the range so that smaller
    values land left of it and larger values right, then recurse on both
    sides. The pivot ends up in its final position after partitioning,
    which we mark as sorted immediately.

    Complexity: O(n log n) average, O(n^2) worst (already sorted input
    with last-element pivot). In-place. Not stable.
    """
    log = StepLogger(array)
    arr = log.array

    def partition(low: int, high: int) -> int:
        """Rearrange arr[low..high] around pivot arr[high], return pivot index.

        Invariant: after the loop, everything in arr[low..i] is <= pivot
        and everything in arr[i+1..high-1] is > pivot. The final swap
        drops the pivot into position i+1.
        """
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            log.compare(j, high)
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    log.swap(i, j)
        if i + 1 != high:
            log.swap(i + 1, high)
        return i + 1

    def sort(low: int, high: int) -> None:
        """Recursive driver; marks the pivot slot sorted after each split."""
        if low < high:
            p = partition(low, high)
            log.mark_sorted(p)
            sort(low, p - 1)
            sort(p + 1, high)
        elif low == high:
            # Single element range is trivially sorted
            log.mark_sorted(low)

    sort(0, len(arr) - 1)
    return log.steps
