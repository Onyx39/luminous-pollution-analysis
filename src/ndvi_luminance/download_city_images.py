"""
Downloads all the images of the cities with custom bands
"""

from json import loads
import logging
from skimage.filters import median
from skimage.io import imsave
from skimage.morphology import square
from tqdm import tqdm

from src.utils import gen_sentinel_req, sentinel_api_setup

from .constants import END_DATE, START_DATE, config


logging.basicConfig(filename="downloadCityImages.log",
                    encoding="utf-8",
                    level=logging.DEBUG,
                    filemode="w")

# Params
EVALSCRIPT_PATH = "luminance2.js"
MAX_CLOUD_COVERAGE = 0.1
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
        (bbox, box_size, download_client, dates) = \
                sentinel_api_setup((START_DATE, END_DATE), city, \
                IMAGE_RESOLUTION, config, MAX_CLOUD_COVERAGE)

        for date in tqdm(dates):
            if date is None:
                continue

            try:
                START_DATE = date.replace(hour=0, minute=0)
                END_DATE = date.replace(hour=6, minute=0)
            except AttributeError: #if hour or mins not in object
                pass

            sentinel_request = gen_sentinel_req((START_DATE, END_DATE),\
                    folder_name, EVALSCRIPT, (bbox, box_size), config)

            img = sentinel_request.get_data(save_data=True)

            print("Downloaded the image")

            # Apply median filter
            img_data = img[0]
            filtered_img = median(img_data, square(7))

            filtered_img_path = folder_name + "/" + city_name + "_filtered.jpg"
            imsave(filtered_img_path, filtered_img)


    except TypeError as e:
        print(e)
        err = f"The forest {city_name} has several segments"
        logging.error(err)
