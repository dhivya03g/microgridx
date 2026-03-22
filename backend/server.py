from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# 🔥 NEW IMPORT (added)
from flask import send_from_directory

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decision_layer.decision_engine import run_decision_engine

app = Flask(__name__)

# 🔥 IMPORTANT: Enable CORS
CORS(app)

@app.route("/")
def home():
    return "MicroGridX Backend Running"


# 🔥 NEW ROUTE (added for frontend)
@app.route("/dashboard")
def dashboard():
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "../digital-twin"),
        "index.html"
    )


@app.route("/api/data")
def get_data():
    try:
        result = run_decision_engine()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


# 🔥 Run server (accessible to frontend)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)