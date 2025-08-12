from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Remove the trailing space and slash so the origin matches exactly
CORS(app, origins=[
    "http://localhost:3001",
    "https://fin-frontend.netlify.app"
])

def calculate_finance_cost(categories):
    total_monthly_cost = 0
    for category, amount in categories.items():
        # if amount is empty string or None, treat as zero
        total_monthly_cost += float(amount or 0)
    return total_monthly_cost

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    categories = data.get("categories", {})
    total = calculate_finance_cost(categories)

    # Return both breakdown and total
    return jsonify({
        "breakdown": categories,
        "total": total
    })

if __name__ == '__main__':
    # In production, set debug=False
    app.run(port=5001, debug=True)
