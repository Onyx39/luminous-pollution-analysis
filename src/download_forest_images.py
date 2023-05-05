""" 
    Downloads all the images of the cities with custom bands for NDVI
"""

import datetime as dt
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
    WebFeatureService
)
from tqdm import tqdm
from constants import config, START_DATE, END_DATE
from utils import get_bbox_from_geojson

logging.basicConfig(filename="downloadForestImages.log",
                    encoding="utf-8",
                    level=logging.DEBUG,
                    filemode="w")

EVALSCRIPT_PATH = "ndvi.js"
MAX_CLOUD_COVERAGE = 0.3
IMAGE_RESOLUTION = 10

EVALSCRIPT = ""
with open("src/evalscripts/"+EVALSCRIPT_PATH, "r", encoding="utf-8") as f:
    EVALSCRIPT = f.read()

all_forests = []
with open("data/forests/forests.json", "r", encoding="utf-8") as f:
    all_forests = loads(f.read())

for i in tqdm(range(len(all_forests))):
    forest = all_forests[i]
    forest_name = forest["properties"]["nom"]
    print("Forest:", forest_name)
    folder_name = "data/images/imagesNDVI/" + forest_name

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

        for date in tqdm(dates):
            start_date = date + dt.timedelta(minutes=-5)
            end_date = date + dt.timedelta(minutes=5)

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
    except TypeError as e:
        print(e)
        err = f"The forest {forest_name} has several segments"
        logging.error(err)
