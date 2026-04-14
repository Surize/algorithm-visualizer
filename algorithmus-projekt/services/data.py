import random


def generate_array(size: int) -> list[int]:
    """Build a shuffled list of unique integers used as the input dataset.

    The size is clamped to [8, 64] so the visualizer never receives
    something too small to be interesting or too large to render fluidly.
    Values are spaced in steps of 5 (5, 10, 15, ...) so the bar heights
    visibly differ even at small counts.
    """
    size = max(8, min(64, int(size)))
    values = list(range(5, size * 5 + 5, 5))
    random.shuffle(values)
    return values
