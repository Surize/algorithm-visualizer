from .base import StepLogger


def merge_sort(array: list[int]) -> list[dict]:
    """Top-down merge sort.

    Recursively split the range in half until each half is trivially
    sorted (size <= 1), then merge the two sorted halves back into one.
    Merging copies the range into a buffer and writes values back using
    `overwrite` so the visualizer can animate values landing in place.

    Complexity: O(n log n) guaranteed. Stable. Uses O(n) auxiliary memory.
    """
    log = StepLogger(array)
    arr = log.array

    def merge(left: int, mid: int, right: int) -> None:
        """Merge arr[left..mid] and arr[mid+1..right] back into arr[left..right].

        We copy the range into a temporary buffer so the two halves are
        untouched while we overwrite the output positions in order.
        """
        buffer = arr[left:right + 1]
        i, j, k = 0, mid - left + 1, left
        size_left = mid - left
        size_right = right - left

        # Interleave the two halves by always taking the smaller head
        while i <= size_left and j <= size_right:
            log.compare(left + i, left + j)
            if buffer[i] <= buffer[j]:
                log.overwrite(k, buffer[i])
                i += 1
            else:
                log.overwrite(k, buffer[j])
                j += 1
            k += 1
        # Drain whichever half still has elements left
        while i <= size_left:
            log.overwrite(k, buffer[i])
            i += 1
            k += 1
        while j <= size_right:
            log.overwrite(k, buffer[j])
            j += 1
            k += 1

    def sort(left: int, right: int) -> None:
        """Recursive divide-and-conquer driver."""
        if left >= right:
            return
        mid = (left + right) // 2
        sort(left, mid)
        sort(mid + 1, right)
        merge(left, mid, right)

    sort(0, len(arr) - 1)
    log.mark_all_sorted()
    return log.steps
