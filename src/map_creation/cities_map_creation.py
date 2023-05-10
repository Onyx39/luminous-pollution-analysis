"""plot cities on a map"""
import folium

from src.utils import MARKER_STYLE, load_data

MARGE = 0.005


# LOAD THE DATA #
print("Opening data file...")
cities = load_data("data/cities/cities_processing_output.json")


# CREATE THE MAP AND FOREST POLYGONS  #

# Create the map
folium_map = folium.Map(location=(46.61, 1.8586), zoom_start=6)

print("Creating map objects...")

WANTED_DEPARTEMENTS = [74, 39]


def add_shape(shape, city, f_map):
    """Add the shape of the city to the map"""
    shape = folium.Polygon(
                shape,
                popup=folium.Popup(city["properties"]["nom"]),
                tooltip=city["properties"]["nom"],
                style_function=lambda: MARKER_STYLE
            )
    shape.add_to(f_map)


def add_city(city, f_map):
    """Add the city to the map"""
    if 'shape' in city['geometry'].keys():
        add_shape(city["geometry"]["shape"][0], city, f_map)

    elif 'MultiShape' in city['geometry'].keys():
        for shape in city["geometry"]["MultiShape"]:
            add_shape(shape, city, f_map)


for city_info in cities:
    if city_info["properties"]["dep"] in WANTED_DEPARTEMENTS:
        add_city(city_info, folium_map)

# SAVING THE MAP
print("Saving file...")
folium_map.save("maps/cities_map.html")

print("Completion of execution : OK")
