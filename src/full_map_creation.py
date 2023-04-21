import json
import folium
from tqdm import tqdm


print("Ouverture du fichier...")
f = open("data_forest/forests.json", encoding='utf-8')
data = json.load(f)


# print(data["features"][0]["geometry"]["coordinates"][0])


marker_style = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}



print("Création des objets à placer sur la carte...")
p_bar = tqdm(total = len(data))
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)
for i in data:
    # print(i["properties"]["nom"])
    if "shape" in i["geometry"].keys():
        shape = folium.Polygon(i["geometry"]["shape"][0],
                            popup=folium.Popup(i["properties"]["nom"]),
                            tooltip=i["properties"]["nom"],
                            style_function=lambda x: marker_style)
        shape.add_to(m)
    
    else : 
        for j in i["geometry"]["MultiShape"][0] :
            shape = folium.Polygon(j,
                                popup=folium.Popup(i["properties"]["nom"]),
                                tooltip=i["properties"]["nom"],
                                style_function=lambda x: marker_style)
            shape.add_to(m)
    p_bar.update(1)

p_bar.close()

print("Sauvegarde du fichier...")
m.save("full_map.html")

print("Fin d'execution : Aucune erreur")
