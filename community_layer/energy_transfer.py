# energy_transfer.py

def transfer_energy(from_house, to_house, amount):

    transfer_data = {
        "from": from_house,
        "to": to_house,
        "energy": amount
    }

    print("Energy transfer successful:")
    print(transfer_data)

# Example
transfer_energy("H001", "H002", 150)