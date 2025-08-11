from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3001"])  # Allow requests from frontend (React)

def calculate_finance_cost(categories):
    total_monthly_cost = 0
    for category, amount in categories.items():
        amount = amount or 0
        total_monthly_cost += float(amount)
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
    app.run(port=5001, debug=True)  # Changed to port 5001