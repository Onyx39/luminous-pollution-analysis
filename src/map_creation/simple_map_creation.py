"""create forest map"""
import folium
from tqdm import tqdm

from src.utils import MARKER_STYLE, load_data

print("Ouverture du fichier...")
data = load_data("data/forests/forests.json")

# Inversion longitude / latitude
for i in data:
    for j in i["geometry"]["coordinates"][0]:
        j[0], j[1] = j[1], j[0]

print("Création des objets à placer sur la carte...")
p_bar = tqdm(total=len(data))
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)
for i in data:
    # print(i["properties"]["nom"])
    shape = folium.Polygon(i["geometry"]["coordinates"],
                           popup=folium.Popup(i["properties"]["nom"]),
                           tooltip=i["properties"]["nom"],
                           style_function=lambda: MARKER_STYLE)
    shape.add_to(m)
    p_bar.update(1)

p_bar.close()

print("Sauvegarde du fichier...")
m.save("maps/simple_map.html")

print("Fin d'execution : Aucune erreur")
