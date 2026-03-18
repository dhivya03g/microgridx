import serial
import json
import time
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================
SERIAL_PORT = "COM5"     # change if your ESP32 is on a different COM port
BAUD_RATE = 115200

# Path to sample_data.json
JSON_PATH = "../data/sample_data.json"

# ==========================
# CONNECT TO ESP32
# ==========================
print("Connecting to ESP32 on", SERIAL_PORT)

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for ESP32 reset

print("Connected! Listening for live sensor data...\n")

# Temporary storage for one full sensor packet
environment_sensor = None
solar_power = None
battery_level = None

while True:
    try:
        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if line:
            print("RAW:", line)

            if line.startswith("environment_sensor="):
                environment_sensor = int(line.split("=")[1])

            elif line.startswith("solar_power="):
                solar_power = float(line.split("=")[1])

            elif line.startswith("battery_level="):
                battery_level = float(line.split("=")[1])

            # Once all 3 values are received, update JSON
            if environment_sensor is not None and solar_power is not None and battery_level is not None:
                with open(JSON_PATH, "r") as file:
                    data = json.load(file)

                # Update live values
                data["timestamp"] = datetime.now().isoformat()
                data["energy_status"]["solar_power"] = round(solar_power, 2)
                data["energy_status"]["battery_level"] = round(battery_level, 2)
                data["energy_status"]["temperature"] = environment_sensor   # using temperature field as environment signal

                # Reset predicted/decision fields for fresh pipeline
                data["energy_status"]["predicted_solar"] = 0
                data["energy_status"]["predicted_demand"] = 0
                data["energy_status"]["energy_score"] = 0

                data["decision"]["energy_mode"] = ""
                data["decision"]["system_action"] = ""
                data["decision"]["battery_action"] = ""

                data["system_health"] = ""
                data["load_priority"]["critical_loads"] = ""
                data["load_priority"]["non_critical_loads"] = ""

                with open(JSON_PATH, "w") as file:
                    json.dump(data, file, indent=4)

                print("\n✅ sample_data.json updated automatically!")
                print("Environment Signal:", environment_sensor)
                print("Solar Power:", solar_power)
                print("Battery Level:", battery_level)
                print("-" * 40)

                # Reset for next packet
                environment_sensor = None
                solar_power = None
                battery_level = None

    except KeyboardInterrupt:
        print("\nStopped by user.")
        break

    except Exception as e:
        print("Error:", e)