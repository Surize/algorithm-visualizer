# Sorting Algorithm Visualizer

Six classic sorting algorithms, implemented from scratch in Python, streamed step-by-step to a thin JavaScript renderer. Watch Bubble, Insertion, Merge, Selection, Quick and Heap Sort race on the same dataset, with per-algorithm runtime measurement.

## Why this project

The point wasn't to draw bars — it was to put the sorting logic where it belongs: **in a testable, modular Python layer**. The browser does nothing except replay the step trace it receives. This split has concrete advantages:

- Every algorithm is a pure function: `sort(array) -> list[steps]`
- Each sort lives in its own file and can be unit-tested in isolation
- The frontend is ~140 lines of vanilla JS — no algorithm logic leaks into it
- Adding a new sort means adding one file and one line in a dispatch dict

## Architecture

```
app.py                      # Flask entry + POST /api/sort endpoint
services/
├── data.py                 # random array generator
└── sorts/
    ├── base.py             # StepLogger: records compare/swap/overwrite/sorted ops
    ├── bubble.py
    ├── insertion.py
    ├── merge.py
    ├── selection.py
    ├── quick.py
    └── heap.py
tests/
└── test_sorts.py           # correctness + JSON serializability (48 cases)
static/
├── css/style.css
└── js/visualizer.js        # fetches step traces, plays them on canvas
templates/
└── index.html
```

### The core idea: `StepLogger`

Each algorithm takes an array and returns a list of operations. A `StepLogger` records every `compare`, `swap`, `overwrite` and `mark_sorted`. The browser replays them against identical initial bars. That means:

- Python owns the algorithm correctness
- The renderer is stateless and trivial to debug
- Steps serialize to JSON and round-trip cleanly (tested)

```python
from services.sorts import ALGORITHMS

steps = ALGORITHMS["quick"]([4, 2, 7, 1, 3])
# → [{"type": "compare", "i": 0, "j": 2}, {"type": "swap", ...}, ...]
```

## Stack

- Python 3.10+
- Flask (HTTP transport only)
- Vanilla JS for rendering (no framework, no build step)
- pytest for the test suite

## Getting Started

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000.

## Running tests

```bash
pytest tests/ -v
```

48 cases covering correctness across edge inputs (empty, single element, already sorted, reverse sorted, duplicates, random) and JSON-serializability for every algorithm.
