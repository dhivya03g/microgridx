import json
from datetime import datetime

# Read input data
with open("data/sample_data.json", "r") as file:
    data = json.load(file)

# Extract values
solar_power = data["energy_status"]["solar_power"]
battery_level = data["energy_status"]["battery_level"]
environment_signal = data["energy_status"]["temperature"]   # using temperature field as live sensor input
humidity = data["energy_status"]["humidity"]
predicted_solar = data["energy_status"]["predicted_solar"]
predicted_demand = data["energy_status"]["predicted_demand"]

# Smart Energy Score
energy_score = round(
    (0.5 * solar_power) +
    (0.3 * battery_level * 10) -
    (0.2 * predicted_demand), 2
)

# Decision Logic
if energy_score >= 150:
    energy_mode = "NORMAL_MODE"
    system_action = "Supply loads and charge battery"
    battery_action = "Charging"
    non_critical_loads = "ON"
    system_health = "GREEN"

elif 80 <= energy_score < 150:
    energy_mode = "ECO_MODE"
    system_action = "Reduce non-critical loads"
    battery_action = "Use battery backup"
    non_critical_loads = "OFF"
    system_health = "YELLOW"

else:
    energy_mode = "EMERGENCY_MODE"
    system_action = "Run critical loads only"
    battery_action = "Battery saving"
    non_critical_loads = "OFF"
    system_health = "RED"

# Update main JSON
data["decision"]["energy_mode"] = energy_mode
data["decision"]["system_action"] = system_action
data["decision"]["battery_action"] = battery_action
data["system_health"] = system_health
data["load_priority"]["critical_loads"] = "ON"
data["load_priority"]["non_critical_loads"] = non_critical_loads
data["energy_status"]["energy_score"] = energy_score

with open("data/sample_data.json", "w") as file:
    json.dump(data, file, indent=4)

# Create decision output file
output = {
    "timestamp": datetime.now().isoformat(),
    "energy_status": data["energy_status"],
    "decision": data["decision"],
    "system_health": data["system_health"],
    "load_priority": data["load_priority"]
}

with open("data/decision_output.json", "w") as file:
    json.dump(output, file, indent=4)

# Console output
print("-------- Decision Layer --------")
print("Solar Power:", solar_power)
print("Battery Level:", battery_level)
print("Environment Signal:", environment_signal)
print("Predicted Demand:", predicted_demand)
print("Energy Score:", energy_score)

print("\nDecision:")
print("Energy Mode:", energy_mode)
print("System Action:", system_action)
print("Battery Action:", battery_action)
print("System Health:", system_health)