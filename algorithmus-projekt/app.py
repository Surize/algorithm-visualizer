from flask import Flask, jsonify, render_template, request

from services import ALGORITHMS, generate_array

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the single-page visualizer UI.

    We pass the list of algorithm keys so the template can render one
    card per algorithm without hard-coding names in HTML.
    """
    return render_template("index.html", algorithms=list(ALGORITHMS.keys()))


@app.route("/api/sort", methods=["POST"])
def sort_api():
    """Run every registered algorithm on the same dataset and return step traces.

    Body (JSON, all optional):
        - array: pre-built list of integers to sort
        - size:  generate a random array of this length instead

    Response:
        {
          "array": [...],
          "algorithms": {
            "bubble":    {"steps": [...]},
            "insertion": {"steps": [...]},
            ...
          }
        }
    """
    payload = request.get_json(silent=True) or {}
    array = payload.get("array")
    if not isinstance(array, list) or not array:
        array = generate_array(payload.get("size", 24))

    # Run each algorithm on the same input so the frontend can race them
    result = {
        name: {"steps": run(array)}
        for name, run in ALGORITHMS.items()
    }
    return jsonify({"array": array, "algorithms": result})


if __name__ == "__main__":
    app.run(debug=True)
