from .base import StepLogger


def heap_sort(array: list[int]) -> list[dict]:
    """Binary max-heap sort.

    Treat the array as a binary tree where node i has children at
    (2i+1) and (2i+2). First we bubble every parent down into a valid
    max-heap (heapify) so the largest value ends up at index 0. Then we
    repeatedly swap the root with the last unsorted slot, shrink the
    heap, and re-heapify. Each extraction pins one more element in its
    final position at the tail.

    Complexity: O(n log n) guaranteed. In-place. Not stable.
    """
    log = StepLogger(array)
    arr = log.array
    n = len(arr)

    def heapify(length: int, root: int) -> None:
        """Restore the max-heap property for the subtree rooted at `root`.

        Compare the root with its two children (if they exist), swap with
        the largest if needed, then recurse down into the affected
        subtree. `length` is the logical size of the heap -- anything at
        or past this index is already sorted and must not move.
        """
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < length:
            log.compare(largest, left)
            if arr[left] > arr[largest]:
                largest = left
        if right < length:
            log.compare(largest, right)
            if arr[right] > arr[largest]:
                largest = right

        if largest != root:
            log.swap(root, largest)
            heapify(length, largest)

    # Build the initial max-heap bottom-up from the last internal node
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # Repeatedly pull the max to the end, shrink the heap, re-heapify
    for end in range(n - 1, 0, -1):
        log.swap(0, end)
        log.mark_sorted(end)
        heapify(end, 0)
    log.mark_sorted(0)

    return log.steps
