from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/predict-demand')
def predict():
    return jsonify({
        "current_demand": 0.82,
        "predicted_demand": 0.94,
        "status": "Demand Increase Expected"
    })

if __name__ == "__main__":
    app.run(debug=True)