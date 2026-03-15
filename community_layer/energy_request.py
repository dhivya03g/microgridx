# energy_request.py

def request_energy(house_id, amount):
    request = {
        "house_id": house_id,
        "requested_energy": amount
    }

    print("Energy request created:")
    print(request)

# Example request
request_energy("H002", 150)