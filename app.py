import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/calculate": {
        "origins": "https://fin-frontend.netlify.app"
    }
})   # <-- this will inject CORS headers on ALL routes, including OPTIONS

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    categories = data.get("categories", {})
    total = calculate_finance_cost(categories) # type: ignore
    return jsonify({ "breakdown": categories, "total": total })

if __name__ == '__main__':
    # use the PORT Render gives you, and listen on 0.0.0.0 so it's publicly reachable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
