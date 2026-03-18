from flask import Blueprint, jsonify, request

community = Blueprint("community", __name__)

# -----------------------------
# SAMPLE DATA
# -----------------------------

houses = [
    {"house_id": "H001", "solar": 5, "usage": 3},
    {"house_id": "H002", "solar": 2, "usage": 4},
    {"house_id": "H003", "solar": 6, "usage": 2}
]

battery = {
    "level": 50,
    "capacity": 100
}

# -----------------------------
# GET HOUSES
# -----------------------------

@community.route("/houses")
def get_houses():
    return jsonify(houses)

# -----------------------------
# ADD HOUSE
# -----------------------------

@community.route("/add-house", methods=["POST"])
def add_house():

    new_house = {
        "house_id": f"H{len(houses)+1:03}",
        "solar": 0,
        "usage": 0
    }

    houses.append(new_house)

    return jsonify(new_house)

# -----------------------------
# ENERGY MATCHING
# -----------------------------

@community.route("/energy-match")
def energy_match():

    transfers = []

    # calculate surplus
    for h in houses:
        h["surplus"] = h["solar"] - h["usage"]

    surplus = [h for h in houses if h["surplus"] > 0]
    deficit = [h for h in houses if h["surplus"] < 0]

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

    # battery logic
    for h in houses:

        surplus = h["solar"] - h["usage"]

        if surplus > 0:
            battery["level"] += min(surplus, battery["capacity"] - battery["level"])

        elif surplus < 0:
            battery["level"] -= min(abs(surplus), battery["level"])

    return jsonify(transfers)