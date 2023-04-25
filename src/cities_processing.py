import json
from tqdm import tqdm
from shapely.geometry import shape


def reduce_shape(geometry):
    """Reduce the number of points of the given shape
    Returns: a list of coordinates
    """
    coords = None
    ratio = 0.001

    coords = geometry.simplify(ratio, preserve_topology=True)

    res = []

    for coord in coords.exterior.coords:
        res.append([coord[1], coord[0]])
    return res


def reduce_multi_shape(geometry):
    """Applies the reduce shape function on a MultiPolygon
    Returns: a list a reduced shape
    """
    res = []
    for geom in geometry.geoms:
        res.append(reduce_shape(geom))
    return res

def init_coordonates(geometry):
    """Initialize the new coordinates and the list of points to visit
    Returns: The list of points to visit and the initialisation of the new coordonates
    """
    coord = geometry["coordinates"]
    if geometry["type"] == "MultiPolygon":
        liste_a_parcourir = []
        for k in coord:
            liste_a_parcourir += k[0]
            points_cardinaux = [coord[0][0][0][0], coord[0][0][0][0],
                               coord[0][0][0][1], coord[0][0][0][1]]
        return liste_a_parcourir, points_cardinaux

    liste_a_parcourir = coord[0]
    points_cardinaux = [coord[0][0][0], coord[0][0][0],
                       coord[0][0][1], coord[0][0][1]]
    return liste_a_parcourir, points_cardinaux



def create_cities_file():
    """Create a json file that contains all needed data about cities
    Returns: boolean (creates automatically the file)
    """
    # Link of the data:
    # https://github.com/gregoiredavid/france-geojson/blob/master/communes.geojson
    print("Importing data...")
    with open("data/cities/communes.geojson", encoding="utf-8") as file:
        data = json.load(file)

    cities_list = []

    for i in data["features"]:
        cities_list.append([i["properties"], i["geometry"]])

    print("Writing file...")
    with open('data/cities/cities_output_Valentin.json', 'w',encoding='utf-8') as json_file:
        json_file.write("[\n")
        compteur = 1
        p_bar = tqdm(total=len(cities_list))
        for [prop, geom] in cities_list:
            liste_a_parcourir, points_cardinaux = init_coordonates(geom)

            for k in liste_a_parcourir:
                if k[0] < points_cardinaux[0]:
                    points_cardinaux[0] = k[0]
                if k[0] > points_cardinaux[1]:
                    points_cardinaux[1] = k[0]
                if k[1] < points_cardinaux[2]:
                    points_cardinaux[2] = k[1]
                if k[1] > points_cardinaux[3]:
                    points_cardinaux[3] = k[1]

            if prop["code"][:2] == "2A" or prop["code"][:2] == "2B":
                dep = 20
            else:
                dep = int(prop["code"][:2])

            polygon = {
                "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                    [
                                        [points_cardinaux[1],
                                         points_cardinaux[3]],
                                        [points_cardinaux[0],
                                         points_cardinaux[3]],
                                        [points_cardinaux[0],
                                         points_cardinaux[2]],
                                        [points_cardinaux[1],
                                         points_cardinaux[2]]
                                    ]
                                ],
                            },
                        "properties": {
                            "nom": prop["nom"],
                            "dep": dep
                        }
                    }

            if geom["type"] == 'MultiPolygon':
                polygon['geometry']['MultiShape'] = [reduce_multi_shape(shape(geom))]

            else:
                polygon['geometry']['shape'] = [reduce_shape(shape(geom))]

            json.dump(polygon, json_file, ensure_ascii=False)
            compteur += 1
            if compteur != len(cities_list) + 1:
                json_file.write(",\n")
            p_bar.update(1)

        json_file.write("\n]")

    p_bar.close()
    file.close()
    print("End of execution: no error")
    return True


create_cities_file()
