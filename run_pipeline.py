import serial
import json
import time
import subprocess
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================
SERIAL_PORT = "COM5"      # Change if your ESP32 is on a different port
BAUD_RATE = 115200

SAMPLE_JSON = "data/sample_data.json"

print(f"Connecting to ESP32 on {SERIAL_PORT}...")

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # wait for ESP32 reset
    print("Connected! Listening for live sensor data...\n")
except Exception as e:
    print("❌ Could not open serial port:", e)
    print("Make sure:")
    print("1. ESP32 is connected")
    print("2. Arduino Serial Monitor is CLOSED")
    print("3. COM port is correct")
    exit()

# Temporary packet storage
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

            # Once one full packet is received
            if environment_sensor is not None and solar_power is not None and battery_level is not None:
                # ==========================
                # UPDATE sample_data.json
                # ==========================
                with open(SAMPLE_JSON, "r") as file:
                    data = json.load(file)

                data["timestamp"] = datetime.now().isoformat()
                data["energy_status"]["solar_power"] = round(solar_power, 2)
                data["energy_status"]["battery_level"] = round(battery_level, 2)
                data["energy_status"]["temperature"] = environment_sensor   # using temperature field as environment signal

                # Reset prediction + decision values before fresh run
                data["energy_status"]["predicted_solar"] = 0
                data["energy_status"]["predicted_demand"] = 0
                data["energy_status"]["energy_score"] = 0

                data["decision"]["energy_mode"] = ""
                data["decision"]["system_action"] = ""
                data["decision"]["battery_action"] = ""

                data["system_health"] = ""
                data["load_priority"]["critical_loads"] = ""
                data["load_priority"]["non_critical_loads"] = ""

                with open(SAMPLE_JSON, "w") as file:
                    json.dump(data, file, indent=4)

                print("\n✅ sample_data.json updated!")

                # ==========================
                # RUN THINKING LAYER
                # ==========================
                print("\n🧠 Running Thinking Layer...")
                subprocess.run(["python", "thinking_layer/prediction_model.py"], check=True)

                # ==========================
                # RUN DECISION LAYER
                # ==========================
                print("\n⚡ Running Decision Layer...")
                subprocess.run(["python", "decision_layer/decision_engine.py"], check=True)

                print("\n🎯 Pipeline cycle completed successfully!")
                print("=" * 50)

                # Reset packet for next cycle
                environment_sensor = None
                solar_power = None
                battery_level = None

    except KeyboardInterrupt:
        print("\nStopped by user.")
        break

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(1)