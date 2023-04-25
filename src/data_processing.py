import json
from tqdm import tqdm
from shapely.geometry import shape
from typing import Callable


def filter(lmbd: Callable, data: list) -> list:
    res = []
    for k in data:
        if lmbd(k):
            res.append(k)
    return res


def reduce_shape(geometry, ratio=0.001) -> list[list[int]]:
    """Reduce the number of points of the given shape
    Returns: a list of coordinates
    """
    reduced_shape = geometry.simplify(
            ratio, preserve_topology=True
    )

    # Inverting the coordinates
    return [[c[1], c[0]] for c in reduced_shape.exterior.coords]


def reduce_multi_shape(geometry) -> list[list[list[int]]]:
    """Applies the reduce shape function on a MultiPolygon
    Returns: a list a reduced shape
    """
    res = []
    for geom in geometry.geoms:
        res.append(reduce_shape(geom))
    return res


def open_forest_file(path):
    """Open forest file and return the list of forests"""
    print("Reading data...")
    with open(path, encoding="utf-8") as forest_file:
        data = json.load(forest_file)

    return data["features"]


def treat_forest_data(forest):
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
                    "nom": forest["properties"]["llib_frt"]
                }
            }

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
            polygon = treat_forest_data(forest)

            json.dump(polygon, json_file, ensure_ascii=False)
            count += 1
            if not count == len(forest_list) + 1:
                json_file.write(",\n")
            p_bar.update(1)

        json_file.write("\n]")

        p_bar.close()
        print("Fin d'execution : Aucune erreur")


def main():
    """Main function"""
    forest_list = open_forest_file("data/forest/FOR_PUBL_FR.json")

    write_json(forest_list)


data = []
if __name__ == "__main__":
    main()

    # example of filter
    # data = open_forest_file("data/data_forest/FOR_PUBL_FR.json")

    # lmbd = lambda x: x["properties"]["cinse_dep"] == "39"
    # res = filter(lmbd, data)
