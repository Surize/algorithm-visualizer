from .base import StepLogger


def selection_sort(array: list[int]) -> list[dict]:
    """Selection sort.

    In every outer pass we scan the unsorted suffix for the smallest
    element and swap it into the first unsorted slot. This makes exactly
    one swap per pass (or zero if the minimum is already there) and
    n*(n-1)/2 comparisons regardless of input -- so its running time is
    unaffected by the data distribution.

    Complexity: O(n^2) always. In-place. Not stable.
    """
    log = StepLogger(array)
    arr = log.array
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            log.compare(min_idx, j)
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            log.swap(i, min_idx)
        log.mark_sorted(i)

    return log.steps
