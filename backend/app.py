from flask import Flask, jsonify, request

app = Flask(__name__)

houses = [
    {"house_id": "H001", "solar": 500, "usage": 300},
    {"house_id": "H002", "solar": 200, "usage": 350},
    {"house_id": "H003", "solar": 400, "usage": 200}
]


@app.route("/")
def home():
    return "MicroGridX Community Energy API Running"


@app.route("/houses")
def get_houses():
    return jsonify(houses)


@app.route("/energy-match")
def energy_match():

    for house in houses:
        house["surplus"] = house["solar"] - house["usage"]

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


if __name__ == "__main__":
    app.run(debug=True)