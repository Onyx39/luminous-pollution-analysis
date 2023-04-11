import json
from tqdm import tqdm

def create_forest_file():
    print("Importation des données...")
    file = open("data_forest/FOR_PUBL_FR.json", encoding="utf-8")
    data = json.load(file)

    forest_list = []

    for i in data["features"]:
        forest_list.append([i["properties"]["llib_frt"], i["geometry"]["coordinates"], i["geometry"]["type"]])

    print("Ecriture du fichier...")
    with open('data_forest/forests.json', 'w', encoding='utf-8') as json_file:
        json_file.write("[\n")
        compteur = 1
        p_bar = tqdm(total = len(forest_list))
        for j in forest_list:
            if j[2] == "MultiPolygon":
                liste_a_parcourir = []
                for k in j[1] :
                    liste_a_parcourir += k[0]
                point_cardinaux = [j[1][0][0][0][0], j[1][0][0][0][0], 
                                   j[1][0][0][0][1], j[1][0][0][0][1]]

            else : 
                liste_a_parcourir = j[1][0]
                point_cardinaux = [j[1][0][0][0], j[1][0][0][0],
                                   j[1][0][0][1], j[1][0][0][1]]
            
            for k in liste_a_parcourir:
                if k[0] < point_cardinaux[0]:
                    point_cardinaux[0] = k[0]
                if k[0] > point_cardinaux[1]:
                    point_cardinaux[1] = k[0]
                if k[1] < point_cardinaux[2]:
                    point_cardinaux[2] = k[1]
                if k[1] > point_cardinaux[3]:
                    point_cardinaux[3] = k[1]

            polygon = {"type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates":
                        [
                            [
                                [point_cardinaux[1], point_cardinaux[3]],
                                [point_cardinaux[0], point_cardinaux[3]],
                                [point_cardinaux[0], point_cardinaux[2]],
                                [point_cardinaux[1], point_cardinaux[2]]
                            ]
                        ]
                    },
                    "properties":  {
                        "nom": j[0]
                    }
                    }
            json.dump(polygon, json_file, ensure_ascii=False)
            compteur += 1
            if not compteur == len(forest_list) + 1 :
                json_file.write(",\n")
            p_bar.update(1)
                
        json_file.write("\n]")

    p_bar.close()
    file.close()
    print("Fin d'execution : Aucune erreur")
    return True


create_forest_file()

