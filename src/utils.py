"""
this module is for general data processing.
It is usefull since we have to do a lot of the same data manipulation.
"""
from datetime import date
import json
from typing import Any, List
import folium
from sentinelhub.api.base_request import InputDataDict
from sentinelhub.api.process import SentinelHubRequest
from sentinelhub.api.wfs import WebFeatureService
from sentinelhub.constants import CRS, MimeType, MosaickingOrder
from sentinelhub.data_collections import DataCollection
from sentinelhub.download.sentinelhub_client import SentinelHubDownloadClient
from sentinelhub.geo_utils import bbox_to_dimensions
from sentinelhub.geometry import BBox


MARKER_STYLE = {
        'fillColor': "#00FF00",
        'color': "#006400",
        'weight': 1,
        'fillOpacity': 0.5}



def fetch_sentinel_dates(dates: tuple[date|str, date|str], bbox,
                       max_cloud_coverage: float, config: Any):
    """
    fetch required dates from sentinel hub api, before fetching data.
    """
    return WebFeatureService(
        bbox=bbox,
        time_interval=(dates[0], dates[1]),
        data_collection=DataCollection.SENTINEL2_L2A,
        maxcc=max_cloud_coverage,
        config=config
    ).get_dates()

def gen_sentinel_input(start_date, end_date) -> List[InputDataDict]:
    """
    retunrs input data for sentinelhub reqs
    """
    return [
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=(str(start_date), str(end_date)),
            mosaicking_order=MosaickingOrder.LEAST_CC,
        )
    ]

def gen_sentinel_req(dates: tuple[date|str, date|str],
                     folder_name: str,
                     evalscript,
                     box: tuple[Any, tuple[int, int]],
                     config: Any):
    """performs a req on sentinelhub"""
    tmp = gen_sentinel_input(dates[0], dates[1])
    return SentinelHubRequest(
        data_folder=folder_name,
        evalscript=evalscript,
        input_data=tmp,
        responses=[
            SentinelHubRequest.output_response("default", MimeType.JPG)
        ],
        bbox=box[0],
        size=box[1],
        config=config,
    )


def sentinel_api_setup(dates: tuple[date|str, date|str], location:Any, res:int,
                       config:Any, max_cloud_coverage: float):
    """
    setup everything and makes sent api calls. Useful for
    dwn_forest and dwn_cities
    """
    boundingbox = get_bbox_from_geojson(location)

    bbox = BBox(bbox=boundingbox, crs=CRS.WGS84)
    box_size = bbox_to_dimensions(bbox, resolution=res)

    download_client = SentinelHubDownloadClient(config=config)

    # Query WFS for available scenes

    dates_out = fetch_sentinel_dates((dates[0], dates[1]), bbox,
                                 max_cloud_coverage, config)

    return (bbox, box_size, download_client, dates_out)


def load_data(path) -> dict:
    """
    Returns a data_dictionary that contains the data of a json file.

        Parameter:
                path (string) : The file path

        Returns:
                data_dictionary (dictionary): The json data of the file
    """
    with open(path, encoding="utf-8") as file:
        data_dictionary = json.load(file)
        return data_dictionary


def handle_polygon_forest(forest_dictionary):
    """
    Returns a polygon that represents a forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon (folium.Polygon): The forest representation for the map
    """
    polygon = folium.Polygon(
                forest_dictionary["geometry"]["shape"][0],
                popup=folium.Popup(forest_dictionary["properties"]["nom"]),
                tooltip=forest_dictionary["properties"]["nom"],
                style_function=lambda: MARKER_STYLE
            )
    return polygon


def handle_multipolygon_forest(forest_dictionary):
    """
    Returns a list that contains all the parts of the forest.

        Parameter:
                forest_dictionary (dictionary) : The forest representation

        Returns:
                polygon_list (list of folium.Polygon): The forest
                representation for the map
    """
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
    """
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

def get_bbox_from_geojson(geojson):
    """
    Gets a geojson object and returns a bbox
    (longitude 1, latitude 1, longitude 2, latitude 2)
    """
    # Initialize the min and max coordinates
    minx, miny = float('inf'), float('inf')
    maxx, maxy = float('-inf'), float('-inf')

    # Loop over the features to find the minimum and maximum coordinates
    if geojson.get('geometry', {}).get('type') == 'Polygon':
        coords = geojson['geometry']['coordinates'][0]
        for coord in coords:
            if coord[0] < minx:
                minx = coord[0]
            if coord[1] < miny:
                miny = coord[1]
            if coord[0] > maxx:
                maxx = coord[0]
            if coord[1] > maxy:
                maxy = coord[1]

    return minx, miny, maxx, maxy
