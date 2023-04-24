from json import loads
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from json import dumps

def distance(lat1, lon1, lat2, lon2):
    # rayon de la Terre en kilomètres
    R = 6371

    # conversion des degrés en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # calcul des différences de latitude et de longitude
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 

    # application de la formule de Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    distance = R * c

    return distance

cities = [] 
with open("../data/cities_data/cities_output.json", "r", encoding="utf-8") as f:
    cities = loads(f.read())

forests = []
with open("forests_ndvi.json", "r", encoding="utf-8") as f:
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

with open("cities_forests.json", "w", encoding = "utf-8") as file:
    file.write(dumps(cities_forests, indent = 4))
