from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from sklearn.linear_model import LinearRegression
from community_layer.community import community

# -----------------------------
# CREATE APP
# -----------------------------

app = Flask(__name__)
CORS(app)

# -----------------------------
# REGISTER BLUEPRINT
# -----------------------------

app.register_blueprint(community)

# -----------------------------
# DATA
# -----------------------------

houses = [
    {"house_id": "H001", "solar": 500, "usage": 300},
    {"house_id": "H002", "solar": 200, "usage": 350},
    {"house_id": "H003", "solar": 400, "usage": 200}
]

battery = {
    "capacity": 1000,
    "level": 500
}

# -----------------------------
# AI MODEL
# -----------------------------

days = np.array([1,2,3,4,5]).reshape(-1,1)
solar_output = np.array([400,420,390,450,470])

model = LinearRegression()
model.fit(days, solar_output)

def predict_solar():
    return round(float(model.predict([[6]])[0]),2)

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def home():
    return "Community Layer Running"

@app.route("/houses")
def get_houses():
    return jsonify(houses)

@app.route("/energy-match")
def energy_match():

    for h in houses:
        h["surplus"] = h["solar"] - h["usage"]

    surplus = [h for h in houses if h["surplus"] > 0]
    deficit = [h for h in houses if h["surplus"] < 0]

    transfers = []

    for s in surplus:
        for d in deficit:
            if s["surplus"] > 0 and d["surplus"] < 0:

                transfer = min(s["surplus"], abs(d["surplus"]))

                transfers.append({
                    "from": s["house_id"],
                    "to": d["house_id"],
                    "energy": transfer
                })

                s["surplus"] -= transfer
                d["surplus"] += transfer

    return jsonify(transfers)

@app.route("/battery-status")
def battery_status():
    return jsonify(battery)

@app.route("/predict-solar")
def predict():
    return jsonify({"predicted": predict_solar()})

# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)