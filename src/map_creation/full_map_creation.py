"""create full forest map. Can handle MultiPolygon."""
import base64
from datetime import datetime
import folium
import folium.features
from tqdm import tqdm
import pandas as pd
from colour import Color

from src.utils import load_data

WIDTH, HEIGHT, FAT_WH = 300, 300, 1.1
DATE = "2023-02-13 00:00:00"

def get_forest_ndvi(forest_name: str, \
        forests_ndvi: pd.DataFrame, date: str) -> float :
    """
    Returns the forest ndvi for one date

    Parameters:
            forest_name (string): The forest name
            forests_ndvi (Panda Dataframe): The dataset with all the 
                forests and their ndvi
            date (str): the date in format "YYYY-mm-dd HH-MM-SS"
    
    Returns:
            The ndvi of the forest or raises an error if the date is not found
    """
    forest_filter = forests_ndvi["nom"] == forest_name
    forest = forests_ndvi[forest_filter]
    try:
        forest = forest.to_dict(orient="records")[0]
    except Exception as exc:
        raise ValueError("Forest not found in ndvi file") from exc
    searched_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    for i in range(len(forest["date"])):
        tmp = datetime.strptime(forest["date"][i], "%Y-%m-%d %H:%M:%S")
        if tmp >= searched_date:
            return forest["ndvi"][i]
    raise ValueError("Date not found")


def get_forest_color(ndvi) -> str:
    """
    Returns a color for an ndvi

    Parameter:
        ndvi: The ndvi of a forest
    
    Returns:
        a color
    """
    color = "#000000"

    if ndvi<-0.5:
        color = Color(rgb=(0.05,0.05,0.05))
    elif ndvi<-0.2:
        color = Color(rgb=(0.75,0.75,0.75))
    elif ndvi<-0.1:
        color = Color(rgb=(0.86,0.86,0.86))
    elif ndvi<0:
        color = Color(rgb=(0.92,0.92,0.92))
    elif ndvi<0.025:
        color = Color(rgb=(1,0.98,0.8))
    elif ndvi<0.05:
        color = Color(rgb=(0.93,0.91,0.71))
    elif ndvi<0.075:
        color = Color(rgb=(0.87,0.85,0.61))
    elif ndvi<0.1:
        color = Color(rgb=(0.8,0.78,0.51))
    elif ndvi<0.125:
        color = Color(rgb=(0.74,0.72,0.42))
    elif ndvi<0.15:
        color = Color(rgb=(0.69,0.76,0.38))
    elif ndvi<0.175:
        color = Color(rgb=(0.64,0.8,0.35))
    elif ndvi<0.2:
        color = Color(rgb=(0.57,0.75,0.32))
    elif ndvi<0.25:
        color = Color(rgb=(0.5,0.7,0.28))
    elif ndvi<0.3:
        color = Color(rgb=(0.44,0.64,0.25))
    elif ndvi<0.35:
        color = Color(rgb=(0.38,0.59,0.21))
    elif ndvi<0.4:
        color = Color(rgb=(0.31,0.54,0.18))
    elif ndvi<0.45:
        color = Color(rgb=(0.25,0.49,0.14))
    elif ndvi<0.5:
        color = Color(rgb=(0.19,0.43,0.11))
    elif ndvi<0.55:
        color = Color(rgb=(0.13,0.38,0.07))
    elif ndvi<0.6:
        color = Color(rgb=(0.06,0.33,0.04))
    else :
        color = Color(rgb=(0,0.27,0))

    return color.hex

def create_forest_popup (forest_dictionary):
    """
    Returns a popup that contains a graph of the evolutoin of NDVI for a forest

    Parameter:
        forest_dictionnary (dictionary): The forest object
    
    Returns:
        a folium.Popup that contains the graph
    """

    forest_name = forest_dictionary["properties"]["nom"]
    file_name = f"data/images/imagesNDVI/{forest_name}/{forest_name}.png"
    with open(file_name, 'rb') as graph :
        encoded = base64.b64encode(graph.read())
        svg = """
        <object data="data:image/jpg;base64,{}" width="{}" height="{} type="image/svg+xml">
        </object>""".format
        iframe = folium.IFrame(svg(encoded.decode('UTF-8'), WIDTH, HEIGHT),
                            width=WIDTH*FAT_WH, height=HEIGHT*FAT_WH)

        return folium.Popup(iframe, parse_html = True, max_width=1500)


def handle_polygon_forest(forest_dictionary) -> folium.Polygon:
    """
    Returns a polygon that represents a forest.

        Parameter:
                forest_dictionary (dictionary): The forest representation

        Returns:
                polygon (folium.Polygon): The forest representation for the map
    """
    try:
        forest_ndvi = get_forest_ndvi(forest_dictionary["properties"]["nom"], \
                data_ndvi, DATE)
        color = get_forest_color(forest_ndvi)

    except ValueError:
        forest_ndvi = "Unknown"
        color = "#7f00ff"

    popup = create_forest_popup(forest_dictionary)

    polygon = folium.Polygon(
                forest_dictionary["geometry"]["shape"][0],
                popup=popup,
                tooltip = f'{forest_dictionary["properties"]["nom"]} \
                            ndvi:{forest_ndvi}',
                color = color,
                fillColor = color,
            )

    return polygon


def handle_multipolygon_forest(forest_dictionary):
    """
    Returns a list that contains all the parts of the forest.

        Parameter:
                forest_dictionary (dictionary): The forest representation

        Returns:
                polygon_list (list of folium.Polygon): The forest
                representation for the map
    """
    polygon_list = []

    try:
        forest_ndvi = get_forest_ndvi(forest_dictionary["properties"]["nom"],\
                data_ndvi, DATE)
        color = get_forest_color(forest_ndvi)

    except ValueError:
        forest_ndvi = "Unknown"
        color = "#7f00ff"

    for polygon in forest_dictionary["geometry"]["MultiShape"][0]:

        popup = create_forest_popup(forest_dictionary)

        polygon = folium.Polygon(
                    polygon,
                    popup=popup,
                    tooltip= f'{forest_dictionary["properties"]["nom"]}\
                            ndvi:{forest_ndvi}',
                    color = color,
                    fillColor = color
                )
        polygon_list.append(polygon)
    return polygon_list


# LOAD THE DATA #
print("Opening data file...")
data_forests = load_data("data/forests/forests.json")

data_ndvi = pd.read_json("data/forests/forests_ndvi.json")


# CREATE THE MAP AND FOREST POLYGONS  #

# Create the map
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)

print("Creating map objects...")

# Display a progress bar
p_bar = tqdm(total=len(data_forests))

for k in data_forests:
    # The forest is a simple polygon
    if "shape" in k["geometry"].keys():
        shape = handle_polygon_forest(k)

        shape.add_to(m)

    # The forest is a MultiPolygon
    else:
        shapes = handle_multipolygon_forest(k)
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
