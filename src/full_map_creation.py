"""create full forest map. Can handle MultiPolygon."""
import folium
import json
import folium.features
from tqdm import tqdm
import pandas as pd
from datetime import datetime
from colour import Color
from math import floor

MARKER_STYLE = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}

DATE = "2023-02-13 00:00:00"

def load_data(path):
    '''
    Returns a data_dictionary that contains the data of a json file.

        Parameter:
                path (string) : The file path

        Returns:
                data_dictionary (dictionary): The json data of the file
    '''
    with open(path, encoding="utf-8") as file:
        data_dictionary = json.load(file)
        return data_dictionary

def get_forest_ndvi(forest_name, forests_ndvi: pd.DataFrame, date) -> float :
    '''
    Returns the forest ndvi for one date

    Parameters:
            forest_name (string) : The forest name
            forests_ndvi (Panda Dataframe): The dataset with all the forests and their ndvi
            date (str): the date in format "YYYY-mm-dd HH-MM-SS"
    
    Returns:
            The ndvi of the forest or raises an error if the date is not found
    '''
    forest_filter = forests_ndvi["nom"] == forest_name
    forest = forests_ndvi[forest_filter]
    try:
        forest = forest.to_dict(orient="records")[0]
    except Exception:
        raise Exception("Forest not found in ndvi file")
    searched_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    
    for i in range(len(forest["date"])):
        d = datetime.strptime(forest["date"][i], "%Y-%m-%d %H:%M:%S")
        if d >= searched_date:
            return forest["ndvi"][i]

    raise Exception("Date not found")

def get_forest_color(ndvi) -> str:
    '''
    Returns a color for an ndvi

    Parameter:
            ndvi: The ndvi of a forest
    
    Returns:
            a color
    '''
    black = Color("black")
    color_range1 = list(black.range_to("white", 4))

    white = Color("white")
    color_range2 = list(white.range_to("green", 20))

    color = "#000000"

    if ndvi < 0:
        index = floor((ndvi+1) * (len(color_range1)-1))
        color = color_range1[index]
    else: 
        index = floor((ndvi) * (len(color_range2)-1))
        color = color_range2[index]

    return color.hex

def handle_polygon_forest(forest_dictionary) -> folium.Polygon:
    '''
    Returns a polygon that represents a forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon (folium.Polygon): The forest representation for the map
    '''
    # forest_ndvi = get_forest_ndvi(forest_dictionary["properties"]["nom"], data_ndvi, DATE)
    # color = get_forest_color(forest_ndvi)
    try:
        forest_ndvi = get_forest_ndvi(forest_dictionary["properties"]["nom"], data_ndvi, DATE)
        color = get_forest_color(forest_ndvi)
    except Exception:
        forest_ndvi = "Unknown"
        color = "#7f00ff"
    polygon = folium.Polygon(
                forest_dictionary["geometry"]["shape"][0],
                popup=folium.Popup(f'{forest_dictionary["properties"]["nom"]} ndvi:{forest_ndvi}'),
                tooltip = f'{forest_dictionary["properties"]["nom"]} ndvi:{forest_ndvi}',
                color = color, 
                fillColor = color,
            )

    return polygon


def handle_multipolygon_forest(forest_dictionary):
    '''
    Returns a list that contains all the parts of the forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon_list (list of folium.Polygon): The forest
                representation for the map
    '''
    polygon_list = []
    # forest_ndvi = get_forest_ndvi(forest_dictionary["properties"]["nom"], data_ndvi, DATE)
    # color = get_forest_color(forest_ndvi)
    try:
        forest_ndvi = get_forest_ndvi(forest_dictionary["properties"]["nom"], data_ndvi, DATE)
        color = get_forest_color(forest_ndvi)
    except Exception:
        forest_ndvi = "Unknown"
        color = "#7f00ff"

    for polygon in forest_dictionary["geometry"]["MultiShape"][0]:

        polygon = folium.Polygon(
                    polygon,
                    popup=folium.Popup(f'{forest_dictionary["properties"]["nom"]} ndvi:{forest_ndvi}'),
                    tooltip= f'{forest_dictionary["properties"]["nom"]} ndvi:{forest_ndvi}',
                    color = color, 
                    fillColor = color
                )
        polygon_list.append(polygon)
    return polygon_list


# LOAD THE DATA #
print("Opening data file...")
data = load_data("data/forest/forests.json")
data_ndvi = pd.read_json("data/forest/forests_ndvi.json")


# CREATE THE MAP AND FOREST POLYGONS  #

# Create the map
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)

print("Creating map objects...")

# Display a progress bar
p_bar = tqdm(total=len(data))

for i in data:
    # The forest is a simple polygon
    if "shape" in i["geometry"].keys():
        shape = handle_polygon_forest(i)
        
        shape.add_to(m)

    # The forest is a MultiPolygon
    else:
        shapes = handle_multipolygon_forest(i)
        for shape in shapes:
            shape.add_to(m)

    # Update the progress bar
    p_bar.update(1)

# Close the progress bar
p_bar.close()

# SAVING THE MAP #
print("Saving file... (might take a while)")
m.save("maps/full_map.html")

print("Completion of execution : OK")
