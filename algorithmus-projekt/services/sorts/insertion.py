from .base import StepLogger


def insertion_sort(array: list[int]) -> list[dict]:
    """Insertion sort.

    Grow a sorted prefix one element at a time. For each new element we
    walk it leftwards through the sorted prefix, swapping with the
    neighbour until it finds its correct slot. Best case on already-sorted
    data is linear because the inner while-loop breaks on the first
    compare.

    Complexity: O(n^2) worst/average, O(n) best. Stable. In-place.
    """
    log = StepLogger(array)
    arr = log.array
    n = len(arr)

    for i in range(1, n):
        j = i
        while j > 0:
            log.compare(j - 1, j)
            if arr[j - 1] > arr[j]:
                log.swap(j - 1, j)
                j -= 1
            else:
                # Found the insertion point -- prefix is sorted again
                break

    log.mark_all_sorted()
    return log.steps
