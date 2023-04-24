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

logging.basicConfig(filename="downloadForestImages.log", encoding="utf-8", level=logging.DEBUG, filemode="w")

config = SHConfig()

config.instance_id = INSTANCE_ID
config.sh_client_id = CLIENT_ID
config.sh_client_secret = USER_SECRET

EVALSCRIPT_PATH = "ndvi.js"
MAX_CLOUD_COVERAGE = 0.3
IMAGE_RESOLUTION = 10

evalscript = ""
with open("evalscripts/"+EVALSCRIPT_PATH, "r", encoding="utf-8") as f:
    evalscript = f.read()

all_forests = []
with open("../data/data_forest/forests.json", "r", encoding="utf-8") as f:
    all_forests = loads(f.read())

for i in range(100):
    forest = all_forests[i]
    forest_name = forest["properties"]["nom"]
    print("Forest:", forest_name)
    folder_name = "imagesNDVI/" + forest_name

    try: 
        boundingbox = get_bbox_from_geojson(forest)

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
            start_date = date + dt.timedelta(hours=-5)
            end_date = date + dt.timedelta(hours=5)

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
        logging.error(f"The forest {forest_name} has several segments")

