from .base import StepLogger


def bubble_sort(array: list[int]) -> list[dict]:
    """Classic bubble sort.

    Walk the list repeatedly, comparing neighbours and swapping when they
    are out of order. After each full pass the largest remaining element
    is in its final place, so the inner loop shrinks by one each iteration.
    An early-exit flag stops the algorithm once a full pass happens
    without any swap -- the list is already sorted.

    Complexity: O(n^2) worst/average, O(n) best. Stable. In-place.
    """
    log = StepLogger(array)
    arr = log.array
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            log.compare(j, j + 1)
            if arr[j] > arr[j + 1]:
                log.swap(j, j + 1)
                swapped = True
        log.mark_sorted(n - i - 1)
        if not swapped:
            # Nothing moved in this pass -> remaining elements are sorted
            for k in range(n - i - 1):
                log.mark_sorted(k)
            break
    return log.steps
