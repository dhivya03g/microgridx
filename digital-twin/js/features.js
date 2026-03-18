from flask import Flask, jsonify
from flask_cors import CORS
from decision_layer.decision_engine import run_decision_engine

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "MicroGridX Backend Running"

@app.route("/api/data")
def data():
    result = run_decision_engine()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)