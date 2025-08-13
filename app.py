from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, resources={
    r"/calculate": {
        "origins": ["https://fin-frontend.netlify.app"]  # add your custom domain if any
    }
})

def calculate_finance_cost(flat_categories: dict) -> float:
    total = 0.0
    for v in flat_categories.values():
        try:
            total += float(v)
        except Exception:
            pass
    return round(total, 2)

@app.route("/calculate", methods=["POST"])
def calculate():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    month = data.get("month")
    categories = data.get("categories")
    if not isinstance(month, str) or not month:
        return jsonify({"error": "Field 'month' must be a non-empty string like '2025-08'"}), 400
    if not isinstance(categories, dict):
        return jsonify({"error": "Field 'categories' must be an object of numbers"}), 400

    total = calculate_finance_cost(categories)
    return jsonify({"breakdown": categories, "total": total}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
