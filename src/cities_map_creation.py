import json
import folium

MARKER_STYLE = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}

MARGE = 0.005

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




### LOAD THE DATA ###
print("Opening data file...")
data = load_data("data/cities_json/cities_output_Valentin.json")


### CREATE THE MAP AND FOREST POLYGONS  ###

# Create the map
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)

print("Creating map objects...")

marker_style = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}

WANTED_DEPARTEMENTS = [74, 39]


for i in data:
    # TODO : il faut gérer les multi polygons !
    if i["properties"]["dep"] in WANTED_DEPARTEMENTS and 'shape' in i['geometry'].keys():
        points = []

        shape = folium.Polygon(i["geometry"]["shape"][0],
                            popup=folium.Popup(i["properties"]["nom"]),
                            tooltip=i["properties"]["nom"],
                            style_function=lambda x: marker_style)
    
        shape.add_to(m)



### SAVING THE MAP ###
print("Saving file...")
m.save("cities_map.html")

print("Completion of execution : OK")
