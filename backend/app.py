from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from sklearn.linear_model import LinearRegression
<<<<<<< HEAD
from community_layer.community import community

# -----------------------------
# CREATE APP
# -----------------------------
=======
>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09

app = Flask(__name__)
CORS(app)

# -----------------------------
<<<<<<< HEAD
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
=======

# House Data

# -----------------------------

houses = [
{"house_id": "H001", "solar": 500, "usage": 300},
{"house_id": "H002", "solar": 200, "usage": 350},
{"house_id": "H003", "solar": 400, "usage": 200}
]

# -----------------------------

# Battery Storage

# -----------------------------

battery = {
"capacity": 1000,
"level": 500
}

# -----------------------------

# AI Solar Prediction Model

# -----------------------------

days = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
solar_output = np.array([400, 420, 390, 450, 470])
>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09

model = LinearRegression()
model.fit(days, solar_output)

def predict_solar():
<<<<<<< HEAD
    return round(float(model.predict([[6]])[0]),2)

# -----------------------------
# ROUTES
=======
    next_day = np.array([[6]])
    prediction = model.predict(next_day)
    return round(float(prediction[0]), 2)

# -----------------------------

# Home API

>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09
# -----------------------------

@app.route("/")
def home():
<<<<<<< HEAD
    return "Community Layer Running"
=======
    return "MicroGridX Community Energy API Running"

# -----------------------------

# Get Houses

# -----------------------------
>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09

@app.route("/houses")
def get_houses():
    return jsonify(houses)

<<<<<<< HEAD
@app.route("/energy-match")
def energy_match():

    for h in houses:
        h["surplus"] = h["solar"] - h["usage"]
=======

# -----------------------------
# Add House
# -----------------------------

@app.route("/add-house", methods=["POST"])
def add_house():

    new_house = {
        "house_id": f"H{len(houses)+1:03}",
        "solar": 0,
        "usage": 0
    }

    houses.append(new_house)

    return jsonify(new_house)


# -----------------------------
# Energy Matching
# -----------------------------

@app.route("/energy-match")
def energy_match():

    for house in houses:
        house["surplus"] = house["solar"] - house["usage"]
>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09

    surplus = [h for h in houses if h["surplus"] > 0]
    deficit = [h for h in houses if h["surplus"] < 0]

    transfers = []

    for s in surplus:
        for d in deficit:
<<<<<<< HEAD
=======

>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09
            if s["surplus"] > 0 and d["surplus"] < 0:

                transfer = min(s["surplus"], abs(d["surplus"]))

                transfers.append({
                    "from": s["house_id"],
                    "to": d["house_id"],
                    "energy": transfer
                })

                s["surplus"] -= transfer
                d["surplus"] += transfer

<<<<<<< HEAD
    return jsonify(transfers)

=======
    # Battery simulation
    for house in houses:

        surplus = house["solar"] - house["usage"]

        if surplus > 0 and battery["level"] < battery["capacity"]:
            charge = min(surplus, battery["capacity"] - battery["level"])
            battery["level"] += charge

        elif surplus < 0 and battery["level"] > 0:
            supply = min(abs(surplus), battery["level"])
            battery["level"] -= supply

    return jsonify(transfers)

# -----------------------------

# Battery Status

# -----------------------------

>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09
@app.route("/battery-status")
def battery_status():
    return jsonify(battery)

<<<<<<< HEAD
@app.route("/predict-solar")
def predict():
    return jsonify({"predicted": predict_solar()})

# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
=======
# -----------------------------

# Solar Prediction

# -----------------------------

@app.route("/predict-solar")
def predict():
    return jsonify({
"predicted_solar": predict_solar()
})

# -----------------------------

# Run Server

# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 4dc9233f686fa7e7e9a20767a44b9d54244dad09
