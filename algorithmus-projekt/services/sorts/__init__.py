from .bubble import bubble_sort
from .insertion import insertion_sort
from .merge import merge_sort
from .selection import selection_sort
from .quick import quick_sort
from .heap import heap_sort

ALGORITHMS = {
    "bubble": bubble_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "selection": selection_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}

__all__ = ["ALGORITHMS"]
