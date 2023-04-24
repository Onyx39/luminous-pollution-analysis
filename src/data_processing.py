import json
from tqdm import tqdm
from shapely.geometry import shape


def reduce_shape(geometry, max_points=20):
    coords = None
    ratio = 0.001

    coords = geometry.simplify(ratio, preserve_topology=True)

    res = []

    for c in coords.exterior.coords:
        res.append([c[1], c[0]])
    return res


def reduce_multi_shape(geometry):
    res = []
    for geom in geometry.geoms:
        res.append(reduce_shape(geom))
    return res


def create_forest_file():
    print("Importation des données...")
    file = open("data_forest/FOR_PUBL_FR.json", encoding="utf-8")
    data = json.load(file)

    forest_list = []

    for i in data["features"]:
        forest_list.append(
                [i["properties"]["llib_frt"],
                 i["geometry"]["coordinates"],
                 i["geometry"]["type"],
                 i["geometry"]])

    print("Ecriture du fichier...")
    with open('data_forest/forests.json', 'w', encoding='utf-8') as json_file:
        json_file.write("[\n")
        compteur = 1
        p_bar = tqdm(total=len(forest_list))
        for j in forest_list:
            if j[2] == "MultiPolygon":
                liste_a_parcourir = []
                for k in j[1]:
                    liste_a_parcourir += k[0]
                point_cardinaux = [j[1][0][0][0][0], j[1][0][0][0][0],
                                   j[1][0][0][0][1], j[1][0][0][0][1]]

            else:
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

            polygon = {
                "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                    [
                                        [point_cardinaux[1],
                                         point_cardinaux[3]],
                                        [point_cardinaux[0],
                                         point_cardinaux[3]],
                                        [point_cardinaux[0],
                                         point_cardinaux[2]],
                                        [point_cardinaux[1],
                                         point_cardinaux[2]]
                                    ]
                                ],
                            },
                        "properties": {
                            "nom": j[0]
                        }
                    }

            if j[2] == 'MultiPolygon':
                polygon['geometry']['MultiShape'] = [
                    reduce_multi_shape(shape(j[3]))
                    ]
            else:
                polygon['geometry']['shape'] = [reduce_shape(shape(j[3]))]

            json.dump(polygon, json_file, ensure_ascii=False)
            compteur += 1
            if not compteur == len(forest_list) + 1:
                json_file.write(",\n")
            p_bar.update(1)

        json_file.write("\n]")

    p_bar.close()
    file.close()
    print("Fin d'execution : Aucune erreur")
    return True


create_forest_file()
