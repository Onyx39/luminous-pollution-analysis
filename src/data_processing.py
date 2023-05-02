"""process forest data"""
import json
from typing import Callable
from tqdm import tqdm
from shapely.geometry import shape
from utils import reduce_shape, create_polygon, reduce_multi_shape


def forest_filter(lmbd: Callable, data: list) -> list:
    """Filter forests based on a lambda function"""
    res = []
    for k in data:
        if lmbd(k):
            res.append(k)
    return res


def open_forest_file(path):
    """Open forest file and return the list of forests"""
    print("Reading data...")
    with open(path, encoding="utf-8") as forest_file:
        data = json.load(forest_file)

    return data["features"]


def process_forest_data(forest):
    """Treat a forest and return a Polygon containing the reduced_shape and a
    square of the forest area"""
    coordinates = forest["geometry"]["coordinates"]
    if forest["geometry"]["type"] == "MultiPolygon":
        liste_a_parcourir = []
        for k in coordinates:
            liste_a_parcourir += k[0]
        point_cardinaux = [coordinates[0][0][0][0], coordinates[0][0][0][0],
                           coordinates[0][0][0][1], coordinates[0][0][0][1]]

    else:
        liste_a_parcourir = coordinates[0]
        point_cardinaux = [coordinates[0][0][0], coordinates[0][0][0],
                           coordinates[0][0][1], coordinates[0][0][1]]

    for k in liste_a_parcourir:
        if k[0] < point_cardinaux[0]:
            point_cardinaux[0] = k[0]
        if k[0] > point_cardinaux[1]:
            point_cardinaux[1] = k[0]
        if k[1] < point_cardinaux[2]:
            point_cardinaux[2] = k[1]
        if k[1] > point_cardinaux[3]:
            point_cardinaux[3] = k[1]

    polygon = create_polygon(point_cardinaux, forest["properties"]["llib_frt"])

    if forest["geometry"]["type"] == 'MultiPolygon':
        polygon['geometry']['MultiShape'] = [
            reduce_multi_shape(shape(forest["geometry"]))
            ]
    else:
        polygon['geometry']['shape'] = [
                reduce_shape(shape(forest["geometry"]))
                ]

    return polygon


def write_json(forest_list):
    """Write the new json forest"""
    print("Writing the file...")
    with open('forest/forests.json', 'w', encoding='utf-8') as json_file:
        json_file.write("[\n")

        count = 1
        p_bar = tqdm(total=len(forest_list))

        for forest in forest_list:
            polygon = process_forest_data(forest)

            json.dump(polygon, json_file, ensure_ascii=False)
            count += 1
            if not count == len(forest_list) + 1:
                json_file.write(",\n")
            p_bar.update(1)

        json_file.write("\n]")

        p_bar.close()
        print("Fin d'execution : Aucune erreur")


if __name__ == "__main__":
    forests = open_forest_file("data/forest/FOR_PUBL_FR.json")

    # lmbd = lambda x: x["properties"]["cinse_dep"] == "39"
    # forests = forest_filter(lmbd, data)

    write_json(forests)
