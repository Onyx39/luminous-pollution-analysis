"""
Downloads all the images of the cities with custom bands
"""

import logging
from json import loads

from skimage.filters import median #pylint: disable=no-name-in-module
from skimage.io import imsave
from skimage.morphology import square
from tqdm import tqdm
from utm.error import OutOfRangeError

from src.utils import gen_sentinel_req, sentinel_api_setup

from .constants import END_DATE, START_DATE, config, DEPARTMENT

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
with open("data/cities/communes.geojson", "r", encoding="utf-8") as f:
    all_cities = loads(f.read())
    all_cities = all_cities["features"]
    all_cities = list(filter(lambda x: x["properties"]["code"]\
            .startswith(DEPARTMENT), all_cities))

for i in tqdm(range(len(all_cities))):
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
            img_start_date = date
            img_end_date = date
            try:
                img_start_date = date.replace(hour=0, minute=0)
                img_end_date = date.replace(hour=6, minute=0)
            except AttributeError: #if hour or mins not in object
                pass

            sentinel_request = gen_sentinel_req((img_start_date, img_end_date),
                    folder_name, EVALSCRIPT, (bbox, box_size), config)

            img = sentinel_request.get_data(save_data=True)

            # Apply median filter
            img_data = img[0]
            filtered_img = median(img_data, square(7))

            filtered_img_path = folder_name + "/" + city_name + "_filtered.jpg"
            imsave(filtered_img_path, filtered_img)


    except TypeError as e:
        print(e)
        err = f"The city {city_name} has several segments"
        logging.error(err)

    except AttributeError as e :
        print(e)
        err = f"The city {city_name} has no geometry"
        logging.error(err)

    except OutOfRangeError as e :
        err = f"The city {city_name} has coordonates out of range"
        logging.error(err)
