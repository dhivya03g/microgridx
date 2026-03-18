import json

# Read current system data
with open("data/sample_data.json", "r") as file:
    data = json.load(file)

# Extract values from energy_status
solar_power = data["energy_status"]["solar_power"]
battery_level = data["energy_status"]["battery_level"]
environment_signal = data["energy_status"]["temperature"]   # using temperature field as live sensor input
humidity = data["energy_status"]["humidity"]

# Predict future solar generation (simple AI logic)
predicted_solar = round(solar_power * 0.75, 2)

# Predict future demand using live environmental signal + humidity
predicted_demand = round((environment_signal * 0.35) + (humidity * 0.6), 2)

# Update JSON
data["energy_status"]["predicted_solar"] = predicted_solar
data["energy_status"]["predicted_demand"] = predicted_demand

with open("data/sample_data.json", "w") as file:
    json.dump(data, file, indent=4)

# Console output
print("-------- Thinking Layer --------")
print("Current Solar Power:", solar_power)
print("Current Battery Level:", battery_level)
print("Environment Signal:", environment_signal)
print("Predicted Solar:", predicted_solar)
print("Predicted Demand:", predicted_demand)