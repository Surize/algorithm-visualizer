"""Verify every algorithm produces steps that yield a sorted array."""
import random

import pytest

from services.sorts import ALGORITHMS


def apply_steps(array: list[int], steps: list[dict]) -> list[int]:
    """Replay a recorded step list against a copy of the input array.

    This mirrors what the browser does when it animates the sort. If the
    result matches Python's built-in `sorted`, the algorithm is correct
    *and* the logged steps are a faithful transcript of what it did.
    """
    arr = list(array)
    for step in steps:
        if step["type"] == "swap":
            i, j = step["i"], step["j"]
            arr[i], arr[j] = arr[j], arr[i]
        elif step["type"] == "overwrite":
            arr[step["i"]] = step["value"]
        # "compare" and "sorted" are annotations -- they do not mutate state
    return arr


@pytest.fixture(params=[
    [],                                        # empty input
    [42],                                      # single element
    [3, 1, 2],                                 # tiny unsorted
    [5, 5, 5, 5],                              # all duplicates
    list(range(10)),                           # already sorted
    list(range(10, 0, -1)),                    # reverse sorted
    [random.randint(0, 100) for _ in range(20)],  # random
])
def sample(request):
    """Edge-case inputs covered by every algorithm test."""
    return request.param


@pytest.mark.parametrize("name,fn", list(ALGORITHMS.items()))
def test_algorithm_sorts_correctly(name, fn, sample):
    """Every registered algorithm must produce a correctly sorted result."""
    steps = fn(sample)
    result = apply_steps(sample, steps)
    assert result == sorted(sample), f"{name} failed on {sample}"


@pytest.mark.parametrize("name,fn", list(ALGORITHMS.items()))
def test_steps_are_serializable(name, fn):
    """Steps must survive a JSON round-trip since they travel over HTTP."""
    import json
    steps = fn([4, 2, 7, 1, 3])
    json.dumps(steps)
