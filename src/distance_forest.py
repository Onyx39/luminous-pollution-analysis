"""
Create a json   
"""

from math import radians, sin, cos, sqrt, atan2
from json import dumps, loads


def distance(latitude1, longitude1, latitude2, longitude2) -> float:
    """ Calculates the distance between 2 coordinates"""
    # radius of the Earth
    earth_radius = 6371

    # degree to radians conversion
    latitude1, longitude1, latitude2, longitude2 = map(radians,
                                                [latitude1, longitude1, latitude2, longitude2])

    # latitude and longitude differences
    dlat = latitude2 - latitude1
    dlon = longitude2 - longitude1

    # Haversine formula
    a_value = sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    c_value = 2 * atan2(sqrt(a_value), sqrt(1-a_value))
    dist = earth_radius * c_value

    return dist

cities = []
with open("data/cities/city_centres.json", "r", encoding="utf-8") as f:
    cities = loads(f.read())

forests = []
with open("data/forests/forests_ndvi.json", "r", encoding="utf-8") as f:
    forests = loads(f.read())

cities_forests = []
for forest in forests:
    lat1 = forest["coords"][1]
    long1 = forest["coords"][0]

    CLOSEST_CITY = None
    DISTANCE = None

    for city in cities:
        lat2 = float(city["latitude"])
        long2 = float(city["longitude"])
        d = distance(lat1, long1, lat2, long2)
        if CLOSEST_CITY is None or DISTANCE > d:
            CLOSEST_CITY = city["label"]
            DISTANCE = d

    cities_forests.append({
        "city" : CLOSEST_CITY, 
        "forest" : forest["nom"],
        "distance" : DISTANCE
    })

if __name__ == "__main__":
    with open("data/forests/cities_forests.json", "w", encoding = "utf-8") as file:
        file.write(dumps(cities_forests, indent = 4))
