"""
Module for gathering lists of cities,
and output to data/cities/cities_processing_output.json
"""
import json

from shapely.geometry import shape
from tqdm import tqdm

from src.utils import create_polygon, reduce_multi_shape, reduce_shape


def init_coordonates(geometry):
    """Initialize the new coordinates and the list of points to visit
    Returns: The list of points to visit and the initialisation of the 
    new coordonates
    """
    coord = geometry["coordinates"]
    if geometry["type"] == "MultiPolygon":
        list_to_iterate = []

        for k in coord:
            list_to_iterate += k[0]

        cardinal_points = [coord[0][0][0][0], coord[0][0][0][0],
                           coord[0][0][0][1], coord[0][0][0][1]]
        return list_to_iterate, cardinal_points

    list_to_iterate = coord[0]
    cardinal_points = [coord[0][0][0], coord[0][0][0],
                       coord[0][0][1], coord[0][0][1]]
    return list_to_iterate, cardinal_points



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
    with open('data/cities/cities_processing_output.json', 'w', \
            encoding='utf-8') as json_file:

        json_file.write("[\n")
        counter = 1
        p_bar = tqdm(total=len(cities_list))

        for [prop, geom] in cities_list:
            liste_a_parcourir, cardinal_points = init_coordonates(geom)

            for k in liste_a_parcourir:
                if k[0] < cardinal_points[0]:
                    cardinal_points[0] = k[0]
                if k[0] > cardinal_points[1]:
                    cardinal_points[1] = k[0]
                if k[1] < cardinal_points[2]:
                    cardinal_points[2] = k[1]
                if k[1] > cardinal_points[3]:
                    cardinal_points[3] = k[1]

            if prop["code"][:2] == "2A" or prop["code"][:2] == "2B":
                dep = 20
            else:
                dep = int(prop["code"][:2])


            polygon = create_polygon(cardinal_points, prop["nom"], dep)

            if geom["type"] == 'MultiPolygon':
                polygon['geometry']['MultiShape'] = \
                        [reduce_multi_shape(shape(geom))]

            else:
                polygon['geometry']['shape'] = [reduce_shape(shape(geom))]

            json.dump(polygon, json_file, ensure_ascii=False)
            counter += 1
            if counter != len(cities_list) + 1:
                json_file.write(",\n")
            p_bar.update(1)

        json_file.write("\n]")

    p_bar.close()
    file.close()
    print("End of execution: no error")
    return True

create_cities_file()
