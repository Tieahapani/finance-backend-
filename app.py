import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow your deployed frontend(s). Add preview URLs if you use Netlify previews.
ALLOWED_ORIGINS = [
    "https://fin-frontend.netlify.app",
    "https://localhost:3000", 
    r"https://.*\.netlify\.app", 
    # "https://<your-custom-domain>",    # add if you have one
    # "http://localhost:3000",           # uncomment for local dev
]
CORS(app, resources={
    r"/calculate": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
    },
    r"/health": {"origins": "*"},
})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

def calculate_finance_cost(flat_categories: dict) -> float:
    """
    Expects a dict like {"Personal": 120.5, "Common": 30, "Groceries": 99}
    Sums numeric values, tolerates numeric strings.
    """
    total = 0.0
    for k, v in flat_categories.items():
        if isinstance(v, (int, float)):
            total += float(v)
        elif isinstance(v, str):
            try:
                total += float(v.strip() or 0)
            except ValueError:
                # non-numeric string -> ignore or raise; here we ignore gracefully
                pass
        else:
            # if a list/dict sneaks in, try to flatten numbers inside
            if isinstance(v, list):
                for x in v:
                    if isinstance(x, (int, float)) or (isinstance(x, str) and x.strip()):
                        try:
                            total += float(x)
                        except Exception:
                            pass
            elif isinstance(v, dict):
                for x in v.values():
                    try:
                        total += float(x)
                    except Exception:
                        pass
    return round(total, 2)

@app.route("/calculate", methods=["POST"])
def calculate():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    # Validate payload shape
    month = data.get("month")
    categories = data.get("categories")
    if not isinstance(month, str) or not month:
        return jsonify({"error": "Field 'month' must be a non-empty string like '2025-08'"}), 400
    if not isinstance(categories, dict):
        return jsonify({"error": "Field 'categories' must be an object of numbers"}), 400

    try:
        total = calculate_finance_cost(categories)
        return jsonify({"breakdown": categories, "total": total}), 200
    except Exception as e:
        app.logger.exception("Error in /calculate")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use the platform PORT; default to 5001 to match your frontend's local BASE
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
