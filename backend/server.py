from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decision_layer.decision_engine import run_decision_engine

app = Flask(__name__)

# 🔥 IMPORTANT: Enable CORS
CORS(app)

@app.route("/")
def home():
    return "MicroGridX Backend Running"

@app.route("/api/data")
def get_data():
    try:
        result = run_decision_engine()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

# 🔥 Run server (accessible to frontend)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)