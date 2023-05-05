"""
Downloads all the images of the cities with custom bands
"""

from json import loads
import logging
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    MimeType,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
    WebFeatureService,
)
from tqdm import tqdm
from constants import config, START_DATE, END_DATE
from utils import get_bbox_from_geojson


logging.basicConfig(filename="downloadCityImages.log",
                    encoding="utf-8",
                    level=logging.DEBUG,
                    filemode="w")

# Params
EVALSCRIPT_PATH = "luminance.js"
MAX_CLOUD_COVERAGE = 0.3
IMAGE_RESOLUTION = 10

EVALSCRIPT = ""

with open("src/evalscripts/" + EVALSCRIPT_PATH, "r", encoding="utf-8") as f:
    EVALSCRIPT = f.read()

all_cities = []
with open("data/cities/ville.json", "r", encoding="utf-8") as f:
    all_cities = loads(f.read())

for i in tqdm(range(100)):
    city = all_cities[i]
    city_name = city["properties"]["nom"]
    print("City:", city_name)
    folder_name = "data/images/imagesLUMINANCE" + "/" + city_name

    try:
        boundingbox = get_bbox_from_geojson(city)

        bbox = BBox(bbox=boundingbox, crs=CRS.WGS84)
        box_size = bbox_to_dimensions(bbox, resolution=IMAGE_RESOLUTION)

        download_client = SentinelHubDownloadClient(config=config)

        # Query WFS for available scenes
        dates = WebFeatureService(
            bbox=bbox,
            time_interval=(START_DATE, END_DATE),
            data_collection=DataCollection.SENTINEL2_L2A,
            maxcc=MAX_CLOUD_COVERAGE,
            config=config
        ).get_dates()

        for date in tqdm(dates):
            start_date = date.replace(hour=0, minute=0)
            end_date = date.replace(hour=6, minute=0)

            sentinel_request = SentinelHubRequest(
                data_folder=folder_name,
                evalscript=EVALSCRIPT,
                input_data=[
                    SentinelHubRequest.input_data(
                        data_collection=DataCollection.SENTINEL2_L2A,
                        time_interval=(str(start_date), str(end_date)),
                        mosaicking_order='leastCC',
                    )
                ],
                responses=[
                    SentinelHubRequest.output_response("default", MimeType.JPG)
                ],
                bbox=bbox,
                size=box_size,
                config=config,
            )

            img = sentinel_request.get_data(save_data=True)

            print("Downloaded the image")
    except TypeError as e:
        print(e)
        err = f"The forest {city_name} has several segments"
        logging.error(err)
