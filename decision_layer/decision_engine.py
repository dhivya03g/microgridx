import json
from datetime import datetime

def run_decision_engine():

    with open("../data/sample_data.json") as f:
        data = json.load(f)

    solar = data["sensor_data"]["solar_power"]
    battery = data["sensor_data"]["battery_level"]
    temp = data["sensor_data"]["temperature"]
    demand = data["prediction_data"]["predicted_demand"]

    # ENERGY SCORE
    energy_score = (0.5 * solar) + (0.3 * battery * 10) - (0.2 * demand)

    # MODE
    if energy_score > 350:
        mode = "NORMAL"
    elif energy_score > 150:
        mode = "ECO"
    else:
        mode = "EMERGENCY"

    # 🔥 1. ENERGY PERSONALITY
    if demand > solar * 1.5:
        personality = "Aggressive Consumer"
    elif solar > demand:
        personality = "Energy Producer"
    else:
        personality = "Balanced Node"

    # 🔮 2. TIME TRAVEL
    future = energy_score - 150
    future_mode = "ECO" if future < 200 else "NORMAL"

    # 🧠 3. ETHICS
    ethical = "Protect critical loads" if mode == "EMERGENCY" else "Normal supply"

    # ⚡ 4. LOSS DETECTOR
    loss = solar - demand
    inefficiency = "Energy Loss" if loss > 100 else "Efficient"

    # 🧬 6. DNA
    dna = [solar, battery, demand]

    # ⚠️ 7. FAILURE SCORE
    failure_score = demand - (solar + battery * 5)
    failure = "HIGH" if failure_score > 200 else "LOW"

    # 🌍 8. CARBON
    carbon = round(solar * 0.0007, 2)

    # 🧠 9. CONFIDENCE
    confidence = min(100, energy_score / 5)

    return {
        "timestamp": datetime.now().isoformat(),
        "energy_status": {
            "solar": solar,
            "battery": battery,
            "temperature": temp,
            "demand": demand,
            "score": energy_score
        },
        "mode": mode,
        "personality": personality,
        "future_mode": future_mode,
        "ethics": ethical,
        "loss": inefficiency,
        "dna": dna,
        "failure": failure,
        "carbon": carbon,
        "confidence": confidence
    }