"""
this module is for general data processing.
It is usefull since we have to do a lot of the same data manipulation.
"""
import json
import folium

MARKER_STYLE = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}


def load_data(path) -> dict:
    '''
    Returns a data_dictionary that contains the data of a json file.

        Parameter:
                path (string) : The file path

        Returns:
                data_dictionary (dictionary): The json data of the file
    '''
    with open(path, encoding="utf-8") as file:
        data_dictionary = json.load(file)
        return data_dictionary


def handle_polygon_forest(forest_dictionary):
    '''
    Returns a polygon that represents a forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon (folium.Polygon): The forest representation for the map
    '''
    polygon = folium.Polygon(
                forest_dictionary["geometry"]["shape"][0],
                popup=folium.Popup(forest_dictionary["properties"]["nom"]),
                tooltip=forest_dictionary["properties"]["nom"],
                style_function=lambda: MARKER_STYLE
            )
    return polygon


def handle_multipolygon_forest(forest_dictionary):
    '''
    Returns a list that contains all the parts of the forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon_list (list of folium.Polygon): The forest
                representation for the map
    '''
    polygon_list = []
    for polygon in forest_dictionary["geometry"]["MultiShape"][0]:
        polygon = folium.Polygon(polygon,
                    popup=folium.Popup(forest_dictionary["properties"]["nom"]),
                    tooltip=forest_dictionary["properties"]["nom"],
                    style_function=lambda: MARKER_STYLE
                )
        polygon_list.append(polygon)
    return polygon_list


def reduce_shape(geometry, ratio=0.001) -> list[list[int]]:
    """Reduce the number of points of the given shape
    Returns: a list of coordinates
    """
    reduced_shape = geometry.simplify(
            ratio, preserve_topology=True
    )

    # Inverting the coordinates
    return [[c[1], c[0]] for c in reduced_shape.exterior.coords]


def reduce_multi_shape(geometry):
    """Applies the reduce shape function on a MultiPolygon
    Returns: a list a reduced shape
    """
    res = []
    for geom in geometry.geoms:
        res.append(reduce_shape(geom))
    return res


def create_polygon(cardinal_points:list, name:str, dep=None) -> dict:
    """create a polygon
    params: point_cardinaux(list), nom"""
    polygon = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [cardinal_points[1],
                         cardinal_points[3]],
                        [cardinal_points[0],
                         cardinal_points[3]],
                        [cardinal_points[0],
                         cardinal_points[2]],
                        [cardinal_points[1],
                         cardinal_points[2]]
                        ]
                    ],
                },
            "properties": {
                "nom": name,
                }
            }

    if dep:
        polygon["properties"]["dep"] = dep

    return polygon
