"""plot cities on a map"""
import folium
from utils import MARKER_STYLE, load_data

MARGE = 0.005


# LOAD THE DATA #
print("Opening data file...")
data = load_data("data/cities/cities_processing_output.json")


# CREATE THE MAP AND FOREST POLYGONS  #

# Create the map
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)

print("Creating map objects...")

WANTED_DEPARTEMENTS = [74, 39]


for i in data:
    # TODO : il faut gérer les multi polygons !
    if i["properties"]["dep"] in WANTED_DEPARTEMENTS and 'shape' \
                                        in i['geometry'].keys():
        points = []

        shape = folium.Polygon(
                    i["geometry"]["shape"][0],
                    popup=folium.Popup(i["properties"]["nom"]),
                    tooltip=i["properties"]["nom"],
                    style_function=lambda: MARKER_STYLE
                )

        shape.add_to(m)

# SAVING THE MAP
print("Saving file...")
m.save("maps/cities_map.html")

print("Completion of execution : OK")
