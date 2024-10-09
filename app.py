from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Constants for CO2 Emission Factors
R = 6371  # Radius of the Earth in kilometers
short_haul_co2_factor = 0.15  # kg CO2 per passenger-km for short-haul
long_haul_co2_factor = 0.10   # kg CO2 per passenger-km for long-haul
average_passengers = 150  # Assumed average number of passengers

# Haversine formula to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distance in kilometers
    return distance

@app.route('/emissions', methods=['GET'])
def calculate_emissions():
    # Extract latitude and longitude from query parameters
    lat1 = float(request.args.get('lat1'))
    lon1 = float(request.args.get('lon1'))
    lat2 = float(request.args.get('lat2'))
    lon2 = float(request.args.get('lon2'))

    # Calculate distance using the Haversine formula
    distance = haversine(lat1, lon1, lat2, lon2)

    # Determine which emission factor to use based on the distance
    if distance <= 1500:
        co2_factor = short_haul_co2_factor
    else:
        co2_factor = long_haul_co2_factor

    # Calculate total CO2 emissions for all passengers
    total_co2_emissions = distance * co2_factor * average_passengers

    # Calculate CO2 emissions per person in tonnes
    co2_per_person_tonnes = total_co2_emissions / 1000 / average_passengers  # Convert kg to tonnes

    return jsonify({
        "distance_km": distance,
        "total_co2_emissions_kg": total_co2_emissions,
        "co2_per_person_tonnes": co2_per_person_tonnes
    })

if __name__ == '__main__':
    app.run(debug=True)
