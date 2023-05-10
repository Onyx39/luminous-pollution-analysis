"""
Downloads all the images of the cities with custom bands for NDVI
"""
import datetime as dt
from json import loads
import logging

from tqdm import tqdm

from src.utils import gen_sentinel_req, sentinel_api_setup

from .constants import END_DATE, START_DATE, config

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

        (bbox, box_size, download_client, dates) = \
                sentinel_api_setup((START_DATE, END_DATE), forest, \
                IMAGE_RESOLUTION, config, MAX_CLOUD_COVERAGE)


        for date in tqdm(dates):
            if date is None:
                continue

            start_date = date + dt.timedelta(minutes=-5)
            end_date = date + dt.timedelta(minutes=5)

            sentinel_request = gen_sentinel_req((start_date, end_date),\
                    folder_name, EVALSCRIPT, (bbox, box_size), config)


            img = sentinel_request.get_data(save_data=True)

    except TypeError as e:
        print(e)
        err = f"The forest {forest_name} has several segments"
        logging.error(err)
