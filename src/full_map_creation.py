import json
import folium
from tqdm import tqdm

MARKER_STYLE = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}

def load_data (path):
    '''
    Returns a data_dictionary that contains the data of a json file.

        Parameter:
                path (string) : The file path

        Returns:
                data_dictionary (dictionary): The json data of the file
    '''
    try:
        with open(path, encoding="utf-8") as file:
            data_dictionary = json.load(file)
            return data_dictionary
    except:
        raise FileNotFoundError from OSError("path not valid in load_data")

def handle_polygon_forest(forest_dictionary):
    '''
    Returns a polygon that represents a forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon (folium.Polygon): The forest representation for the map
    '''
    polygon = folium.Polygon(forest_dictionary["geometry"]["shape"][0],
                            popup=folium.Popup(forest_dictionary["properties"]["nom"]),
                            tooltip=forest_dictionary["properties"]["nom"],
                            style_function=lambda x: MARKER_STYLE)
    return polygon

def handle_multipolygon_forest(forest_dictionary):
    '''
    Returns a list that contains all the parts of the forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon_list (list of folium.Polygon): The forest representation for the map
    '''
    polygon_list =  []
    for polygon in forest_dictionary["geometry"]["MultiShape"][0]:
        polygon = folium.Polygon(polygon,
                                popup=folium.Popup(forest_dictionary["properties"]["nom"]),
                                tooltip=forest_dictionary["properties"]["nom"],
                                style_function=lambda x: MARKER_STYLE)
        polygon_list.append(polygon)
    return polygon_list


### LOAD THE DATA ###
print("Opening data file...")
data = load_data("data/forest/forests.json")


### CREATE THE MAP AND FOREST POLYGONS  ###

# Create the map
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)

print("Creating map objects...")

# Display a progress bar
p_bar = tqdm(total = len(data))

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

### SAVING THE MAP ###
print("Saving file... (might take a while)")
m.save("maps/full_map.html")

print("Completion of execution : OK")
