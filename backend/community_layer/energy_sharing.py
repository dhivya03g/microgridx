import json

# READ INPUT FILE
with open("community_data.json", "r") as f:
    data = json.load(f)

houses = data["houses"]

surplus = []
deficit = []

# CLASSIFY
for h in houses:
    extra = h["solar_power"] - h["demand"]

    if extra > 0:
        surplus.append({"id": h["house_id"], "value": extra})
    else:
        deficit.append({"id": h["house_id"], "value": abs(extra)})

transfers = []

# MATCHING
for s in surplus:
    for d in deficit:
        if s["value"] > 0 and d["value"] > 0:

            transfer = min(s["value"], d["value"])

            transfers.append({
                "from": s["id"],
                "to": d["id"],
                "energy": transfer
            })

            s["value"] -= transfer
            d["value"] -= transfer

# WRITE OUTPUT FILE
output = {
    "energy_transfers": transfers
}

with open("sharing_output.json", "w") as f:
    json.dump(output, f, indent=4)

print("✅ Energy Sharing Output Generated")