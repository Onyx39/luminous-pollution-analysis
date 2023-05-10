"""create full forest map. Can handle MultiPolygon."""
import base64
from datetime import datetime
from math import floor
from typing import List

import folium
import folium.features
import pandas as pd
from colour import Color
from tqdm import tqdm

from src.utils import load_data

WIDTH, HEIGHT, FAT_WH = 300, 300, 1.1
DATE = "2023-02-13 00:00:00"

def get_forest_ndvi(forest_name: str, date: str) -> float :
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
    forest_filter = data_ndvi["nom"] == forest_name
    forest = data_ndvi[forest_filter]
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

def gen_rgb_array(steps: int) -> List[Color]:
    """
    gen an array of colors from green to red, with `steps` steps.
    Param:
        steps: int
    returns:
        the array
    """
    res = []
    for k in range(0,steps):
        res.append(Color(rgb=((steps - k) / steps, k / steps, 0)))
    return res


def get_forest_color(ndvi: float, colors: list,
                     min_value: float, max_value: float) -> str:
    """
    Returns a color for an ndvi

    Parameter:
        ndvi (float): The ndvi of a forest
        colors (list): array of colors, gened w/ gen_rgb_array
        min (float): min ndvi value
        max (float): max ndvi value

    Returns:
        a color in hex (str)
    """
    #rescale max and min
    min_tmp = min_value + abs((min_value + max_value)) / 6
    max_tmp = max_value - abs((min_value + max_value)) / 2.5

    min_value, max_value = min_tmp, max_tmp

    step_len = (max_value - min_value) / len(colors)
    idx = floor((ndvi - min_value) / step_len)

    if idx > len(colors) - 1:
        idx = len(colors) - 1

    elif idx < 0:
        idx = 0

    return colors[idx].hex

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
        <object data="data:image/jpg;base64,{}" width="{}" height="{} \
                type="image/svg+xml">
        </object>""".format
        width = str(int(WIDTH*FAT_WH)) + "px"
        height = str(int(HEIGHT*FAT_WH)) + "px"
        iframe = folium.IFrame(svg(encoded.decode('UTF-8'), WIDTH, HEIGHT),
                            width=width, height=height)

        return folium.Popup(iframe, parse_html = True,
                            max_width=str(1500) + "px")


def handle_polygon_forest(forest_dictionary) -> dict:
    """
    Returns a polygon that represents a forest.

        Parameter:
                forest_dictionary (dictionary): The forest representation

        Returns:
                polygon (folium.Polygon): The forest representation for the map
    """
    try:
        forest_ndvi = get_forest_ndvi(forest_dictionary["properties"]["nom"], \
                DATE)

    except ValueError:
        forest_ndvi = "Unknown"

    popup = create_forest_popup(forest_dictionary)

    tmp = {
            "polygon": forest_dictionary["geometry"]["shape"][0],
            "name": f'{forest_dictionary["properties"]["nom"]}\
                        ndvi:{forest_ndvi}',
            "ndvi": forest_ndvi,
            "popup": popup
         }

    return tmp


def handle_multipolygon_forest(forest_dictionary: dict):
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
                DATE)

    except ValueError:
        forest_ndvi = "Unknown"

    for polygon in forest_dictionary["geometry"]["MultiShape"][0]:

        popup = create_forest_popup(forest_dictionary)


        tmp = {
                "polygon": polygon,
                "name": f'{forest_dictionary["properties"]["nom"]}\
                        ndvi:{forest_ndvi}',
                "ndvi": forest_ndvi,
                "popup": popup
            }
        polygon_list.append(tmp)

    return polygon_list


# LOAD THE DATA #
print("Opening data file...")
data_forests = load_data("data/forests/forests.json")

data_ndvi = pd.read_json("data/forests/forests_ndvi.json")


# CREATE THE MAP AND FOREST POLYGONS  #

# Create the map
m = folium.Map(location=(46.61, 1.8586), zoom_start=6, \
        tiles="CartoDB dark_matter")

print("Creating map objects...")

# Display a progress bar
p_bar_compute = tqdm(total=len(data_forests))

# list storing polygons parameters before constructing them
# useful for list colors (need max / min)
list_pre_polygons = []
ndvi_min, ndvi_max = 999, -999 # init very low / high for ndvi

for item in data_forests:
    # The forest is a simple polygon
    if "shape" in item["geometry"].keys():
        poly_info = handle_polygon_forest(item)
        list_pre_polygons.append(poly_info)
        ndvi_max = max(ndvi_max, poly_info["ndvi"])
        ndvi_min = min(ndvi_min, poly_info["ndvi"])

    # The forest is a MultiPolygon
    else:
        list_res = handle_multipolygon_forest(item)
        for item in list_res:
            list_pre_polygons.append(item)
            ndvi_max = max(ndvi_max, item["ndvi"])
            ndvi_min = min(ndvi_min, item["ndvi"])

    # Update the progress bar
    p_bar_compute.update(1)

# Close the progress bar
p_bar_compute.close()

p_bar_polygons = tqdm(total=len(data_forests))
color_array = gen_rgb_array(20)

for poly in list_pre_polygons:
    color = get_forest_color(poly["ndvi"], color_array, ndvi_min, ndvi_max)

    shape = folium.Polygon(
                poly["polygon"],
                popup=poly["popup"],
                tooltip = poly["name"],
                color = color,
                fillColor = color
                )
    shape.add_to(m)

    p_bar_polygons.update(1)

p_bar_polygons.close()

# SAVING THE MAP #
print("Saving file... (might take a while)")
m.save("maps/full_map.html")

print("Completion of execution : OK")
