class StepLogger:
    """Records sorting operations as a replayable step sequence.

    Every algorithm talks to the logger instead of mutating the array
    directly. This way the algorithm is decoupled from the presentation:
    the browser just replays the recorded steps to produce the animation.
    """

    def __init__(self, array: list[int]) -> None:
        """Snapshot the initial array into a mutable working copy."""
        self.array = list(array)
        self.steps: list[dict] = []

    def compare(self, i: int, j: int) -> None:
        """Record that two indices are being compared (no state change)."""
        self.steps.append({"type": "compare", "i": i, "j": j})

    def swap(self, i: int, j: int) -> None:
        """Swap two elements and log it so the frontend can animate it."""
        self.steps.append({"type": "swap", "i": i, "j": j})
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def overwrite(self, i: int, value: int) -> None:
        """Write a value at an index; used by merge sort when merging buffers."""
        self.steps.append({"type": "overwrite", "i": i, "value": value})
        self.array[i] = value

    def mark_sorted(self, i: int) -> None:
        """Flag a single index as definitively in its final position."""
        self.steps.append({"type": "sorted", "i": i})

    def mark_all_sorted(self) -> None:
        """Convenience helper to mark every index as sorted at once."""
        for i in range(len(self.array)):
            self.mark_sorted(i)
