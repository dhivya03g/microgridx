import json
import random


# Step 1: Read Input Data

with open("../data/sample_data.json", "r") as file:
    data = json.load(file)

# Read from energy_status
solar_power = data["energy_status"]["solar_power"]
battery_level = data["energy_status"]["battery_level"]
temperature = data["energy_status"]["temperature"]

# Step 2: Prediction Logic

# Predict solar output (slight variation)
predicted_solar = solar_power * (0.8 + random.uniform(-0.1, 0.1))

# Predict demand based on temperature
if temperature > 30:
    predicted_demand = solar_power * 0.9 + 100
else:
    predicted_demand = solar_power * 0.7 + 50

# Round values
predicted_solar = round(predicted_solar, 2)
predicted_demand = round(predicted_demand, 2)


# Step 3: Update JSON


data["energy_status"]["predicted_solar"] = predicted_solar
data["energy_status"]["predicted_demand"] = predicted_demand

# Save updated data
with open("../data/sample_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("-------- Thinking Layer --------")
print("Predicted Solar:", predicted_solar)
print("Predicted Demand:", predicted_demand)