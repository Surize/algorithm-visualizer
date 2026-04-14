/**
 * Thin visualizer: fetches step traces from the Python backend and plays
 * them back on the canvas. No sorting logic lives here -- this file is
 * purely a renderer.
 */
(function () {
  // Client-side state kept in a single object for easy inspection in devtools
  const STATE = {
    array: [],
    algorithms: {},
    tempo: 100,
    busy: false,
  };

  const barCount = document.getElementById("bar-count");
  const tempoInput = document.getElementById("delay-scale");
  const tempoLabel = document.getElementById("delay-label");
  const btnRun = document.getElementById("btn-run");
  const btnRandomize = document.getElementById("btn-randomize");

  /** Promise-based sleep used to pace the animation between steps. */
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  /**
   * Request a new dataset + step traces from the backend, then paint the
   * initial bar state for every canvas.
   * @param {number} size  number of bars to generate
   */
  async function loadSteps(size) {
    const response = await fetch("/api/sort", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ size }),
    });
    const data = await response.json();
    STATE.array = data.array;
    STATE.algorithms = data.algorithms;
    renderAll();
  }

  /** Repaint all six canvases with the current (unsorted) dataset. */
  function renderAll() {
    for (const algo of Object.keys(STATE.algorithms)) {
      renderCanvas(algo, STATE.array);
      const timeEl = document.querySelector(`[data-target="${algo}"]`);
      if (timeEl) timeEl.textContent = "–";
    }
  }

  /**
   * Render an array as bars inside a named canvas.
   * @param {string} algo    algorithm key (e.g. "bubble")
   * @param {number[]} values  array to visualize
   */
  function renderCanvas(algo, values) {
    const canvas = document.getElementById(`canvas-${algo}`);
    if (!canvas) return;
    canvas.innerHTML = "";
    const peak = Math.max(...values, 1);
    for (const value of values) {
      const bar = document.createElement("div");
      bar.className = "viz-bar";
      bar.style.height = `${(value / peak) * 100}%`;
      bar.dataset.value = value;
      canvas.appendChild(bar);
    }
  }

  /**
   * Apply a single step (from the backend trace) to the rendered bars.
   * Each step type maps to a visual operation:
   *   compare   -> highlight two bars (no state change)
   *   swap      -> swap heights + values of two bars
   *   overwrite -> write a new value at an index (used by merge sort)
   *   sorted    -> mark an index as final
   * @param {HTMLElement[]} bars  one element per array index
   * @param {object} step         recorded operation from the backend
   */
  function applyStep(bars, step) {
    // Reset transient highlights from the previous step
    bars.forEach((b) => b.classList.remove("compare", "swap"));

    if (step.type === "compare") {
      bars[step.i].classList.add("compare");
      bars[step.j].classList.add("compare");
    } else if (step.type === "swap") {
      const a = bars[step.i];
      const b = bars[step.j];
      [a.style.height, b.style.height] = [b.style.height, a.style.height];
      [a.dataset.value, b.dataset.value] = [b.dataset.value, a.dataset.value];
      a.classList.add("swap");
      b.classList.add("swap");
    } else if (step.type === "overwrite") {
      const peak = Math.max(...bars.map((x) => +x.dataset.value));
      bars[step.i].style.height = `${(step.value / Math.max(peak, step.value)) * 100}%`;
      bars[step.i].dataset.value = step.value;
    } else if (step.type === "sorted") {
      bars[step.i].classList.add("sorted");
    }
  }

  /**
   * Play back the full step trace for one algorithm, measuring wall time.
   * @param {string} algo  algorithm key to replay
   */
  async function playAlgorithm(algo) {
    const canvas = document.getElementById(`canvas-${algo}`);
    const timeEl = document.querySelector(`[data-target="${algo}"]`);
    if (!canvas) return;
    canvas.classList.add("running");

    // Always start from the same clean state so replays are comparable
    renderCanvas(algo, STATE.array);
    const bars = Array.from(canvas.children);
    const steps = STATE.algorithms[algo].steps;
    // Inverted tempo: higher slider value -> shorter delay per step
    const delay = Math.max(2, 240 - STATE.tempo * 2);

    const start = performance.now();
    for (const step of steps) {
      applyStep(bars, step);
      await sleep(delay / 10);
    }
    const elapsed = performance.now() - start;
    canvas.classList.remove("running");
    if (timeEl) timeEl.textContent = `${elapsed.toFixed(0)} ms`;
  }

  /** Race all six algorithms in parallel on the same dataset. */
  async function runAll() {
    if (STATE.busy) return;
    STATE.busy = true;
    await Promise.all(Object.keys(STATE.algorithms).map(playAlgorithm));
    STATE.busy = false;
  }

  // --- UI wiring ---------------------------------------------------------

  // Tempo slider: update label + internal state; delay is computed on play
  tempoInput?.addEventListener("input", (e) => {
    STATE.tempo = +e.target.value;
    if (tempoLabel) tempoLabel.textContent = `Tempo: ${STATE.tempo}%`;
  });

  // "Neue Daten" -> fetch a fresh randomized dataset
  btnRandomize?.addEventListener("click", () => {
    if (STATE.busy) return;
    loadSteps(+barCount.value);
  });

  // Changing bar count also regenerates the dataset
  barCount?.addEventListener("change", () => {
    if (STATE.busy) return;
    loadSteps(+barCount.value);
  });

  // "Vergleich starten" -> run every algorithm
  btnRun?.addEventListener("click", runAll);

  // Per-card "Replay" buttons rerun a single algorithm
  document.querySelectorAll(".viz-replay").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (STATE.busy) return;
      playAlgorithm(btn.dataset.algo);
    });
  });

  // Kick things off with a default dataset of 24 bars
  loadSteps(24);
})();
