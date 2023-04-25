import json
import folium
from tqdm import tqdm


print("Ouverture du fichier...")
f = open("data/ville_json/villes_polygons.json", encoding='utf-8')
coordinates = json.load(f)



marker_style = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}



print("Création des objets à placer sur la carte...")

p_bar = tqdm(total = len(coordinates))
m = folium.Map(location=(46.61, 1.8586), zoom_start=6)
i = -1


for coordinate in coordinates:
    #print(coordinate["properties"]["nom"])
    i+=1
    try :
        if coordinate is None or coordinate["geometry"]["coordinates"] is None \
                or coordinate["properties"]["nom"] is None:
            raise TypeError
        if coordinate["geometry"]["type"] == "MultiPolygon":
            for coord in coordinate["geometry"]["coordinates"]:
                for c in coord[0]:
                    c[0], c[1] = c[1], c[0]
                shape = folium.Polygon(coord,
                                    popup=folium.Popup(coordinate["properties"]["nom"]),
                                    tooltip=coordinate["properties"]["nom"],
                                    style_function=lambda x: marker_style)
            
        else:
            for c in coordinate["geometry"]["coordinates"][0]:
                c[0], c[1] = c[1], c[0]
            shape = folium.Polygon(coordinate["geometry"]["coordinates"],
                            popup=folium.Popup(coordinate["properties"]["nom"]),
                            tooltip=coordinate["properties"]["nom"],
                            style_function=lambda x: marker_style)
    except TypeError:
        print("error on index ", i)
        continue
    except:
        print(coordinate)
        break
    shape.add_to(m)
    p_bar.update(1)


p_bar.close()


print("Sauvegarde du fichier...")
m.save("data/ville_json/cities_out.html")


print("Fin d'execution : Aucune erreur")