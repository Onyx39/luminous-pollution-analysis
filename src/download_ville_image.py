from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    MimeType,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
    WebFeatureService,
)
import datetime as dt
from constants import *
from utils import get_bbox_from_geojson
from json import loads
import logging

logging.basicConfig(filename="downloadCityImages.log", encoding="utf-8", level=logging.DEBUG, filemode="w")

config = SHConfig()

config.instance_id = INSTANCE_ID
config.sh_client_id = CLIENT_ID
config.sh_client_secret = USER_SECRET

# Paramètres
image_type = "imageLUMINANCE"
EVALSCRIPT_PATH = "luminance.js"
MAX_CLOUD_COVERAGE = 0.3
IMAGE_RESOLUTION = 10

evalscript = ""
with open("evalscripts/" + EVALSCRIPT_PATH, "r", encoding="utf-8") as f:
    evalscript = f.read()

all_cities = []
with open("../data/data_forest/ville.json", "r", encoding="utf-8") as f:
    all_cities = loads(f.read())

for i in range(100):
    city = all_cities[i]
    city_name = city["properties"]["nom"]
    print("City:", city_name)
    folder_name = image_type + "/" + city_name

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

        for date in dates:
            start_date = date.replace(hour=0, minute=0)
            end_date = date.replace(hour=6, minute=0)

            sentinel_request = SentinelHubRequest(
                data_folder=folder_name,
                evalscript=evalscript,
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

            print(f"Downloaded the image")
    except TypeError as e:
        print(e)
        logging.error(f"The city {city_name} has several segments")
