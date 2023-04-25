from math import radians, sin, cos, sqrt, atan2
from json import dumps, loads


def distance(lat1, lon1, lat2, lon2) -> float:
    """ Calculates the distance between 2 coordinates"""
    # radius of the Earth
    R = 6371

    # degree to radians conversion
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # latitude and longitude differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c

    return d

cities = []
with open("data/cities/cities_output.json", "r", encoding="utf-8") as f:
    cities = loads(f.read())

forests = []
with open("data/forests/forests_ndvi.json", "r", encoding="utf-8") as f:
    forests = loads(f.read())

cities_forests = []
for forest in forests:
    lat1 = forest["coords"][1]
    long1 = forest["coords"][0]

    closest_city = None
    distance_ = None

    for city in cities:
        lat2 = float(city["latitude"])
        long2 = float(city["longitude"])
        d = distance(lat1, long1, lat2, long2)
        if closest_city is None or distance_ > d:
            closest_city = city["label"]
            distance_ = d

    cities_forests.append({
        "city" : closest_city, 
        "forest" : forest["nom"],
        "distance" : distance_
    })

if __name__ == "__main__":
    with open("data/forests/cities_forests.json", "w", encoding = "utf-8") as file:
        file.write(dumps(cities_forests, indent = 4))
