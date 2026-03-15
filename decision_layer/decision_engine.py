import json
from datetime import datetime

# ---------------------------------------
# Step 1: Read Input Data
# ---------------------------------------

with open("../data/sample_data.json", "r") as file:
    data = json.load(file)

solar_power = data["sensor_data"]["solar_power"]
battery_level = data["sensor_data"]["battery_level"]
temperature = data["sensor_data"]["temperature"]
humidity = data["sensor_data"]["humidity"]

predicted_solar = data["prediction_data"]["predicted_solar"]
predicted_demand = data["prediction_data"]["predicted_demand"]


# ---------------------------------------
# Step 2: Smart Energy Score (Weighted)
# ---------------------------------------

solar_weight = 0.5
battery_weight = 0.3
demand_weight = 0.2

energy_score = (
    solar_weight * solar_power +
    battery_weight * (battery_level * 10) -
    demand_weight * predicted_demand
)


# ---------------------------------------
# Step 3: Decision Logic
# ---------------------------------------

if energy_score >= 350:
    energy_mode = "NORMAL_MODE"
    system_action = "Supply loads and charge battery"
    battery_action = "Charging"
    non_critical_loads = "ON"

elif energy_score >= 150:
    energy_mode = "ECO_MODE"
    system_action = "Reduce non-critical loads"
    battery_action = "Use battery backup"
    non_critical_loads = "OFF"

else:
    energy_mode = "EMERGENCY_MODE"
    system_action = "Run critical loads only"
    battery_action = "Battery saving"
    non_critical_loads = "OFF"


# ---------------------------------------
# Step 4: System Health Indicator
# ---------------------------------------

if energy_mode == "NORMAL_MODE":
    system_health = "GREEN"

elif energy_mode == "ECO_MODE":
    system_health = "YELLOW"

else:
    system_health = "RED"


# ---------------------------------------
# Step 5: Create Output Data
# ---------------------------------------

output = {
    "timestamp": datetime.now().isoformat(),

    "energy_status": {
        "solar_power": solar_power,
        "battery_level": battery_level,
        "temperature": temperature,
        "humidity": humidity,
        "predicted_solar": predicted_solar,
        "predicted_demand": predicted_demand,
        "energy_score": round(energy_score, 2)
    },

    "decision": {
        "energy_mode": energy_mode,
        "system_action": system_action,
        "battery_action": battery_action
    },

    "system_health": system_health,

    "load_priority": {
        "critical_loads": "ON",
        "non_critical_loads": non_critical_loads
    }
}


# ---------------------------------------
# Step 6: Save Decision Output
# ---------------------------------------

with open("../data/decision_output.json", "w") as file:
    json.dump(output, file, indent=4)


# ---------------------------------------
# Step 7: Console Output (Debug)
# ---------------------------------------

print("-------- MicroGridX Decision Layer --------")
print("Solar Power:", solar_power, "W")
print("Battery Level:", battery_level, "%")
print("Predicted Demand:", predicted_demand, "W")

print("\nSmart Energy Score:", round(energy_score, 2))

print("\nDecision:")
print("Energy Mode:", energy_mode)
print("System Action:", system_action)
print("Battery Action:", battery_action)

print("\nSystem Health:", system_health)