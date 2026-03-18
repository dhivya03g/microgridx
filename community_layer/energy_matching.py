# energy_matching.py

houses = [
    {"house_id": "H001", "solar": 500, "usage": 300},
    {"house_id": "H002", "solar": 200, "usage": 350},
    {"house_id": "H003", "solar": 400, "usage": 200},
]


def calculate_surplus():
    for house in houses:
        house["surplus"] = house["solar"] - house["usage"]


def match_energy():
    surplus_houses = [h for h in houses if h["surplus"] > 0]
    deficit_houses = [h for h in houses if h["surplus"] < 0]

    for s in surplus_houses:
        for d in deficit_houses:

            if s["surplus"] > 0 and d["surplus"] < 0:

                transfer = min(s["surplus"], abs(d["surplus"]))

                print(
                    f"Transfer {transfer}W from {s['house_id']} to {d['house_id']}"
                )

                s["surplus"] -= transfer
                d["surplus"] += transfer


calculate_surplus()
match_energy()