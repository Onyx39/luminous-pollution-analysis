"""create full forest map. Can handle MultiPolygon."""
import folium
from tqdm import tqdm

from utils import handle_multipolygon_forest, handle_polygon_forest, load_data

# LOAD THE DATA #
print("Opening data file...")
data = load_data("data/forest/forests.json")


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
