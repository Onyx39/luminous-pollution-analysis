"""
Calculates map NDVI and Luminance
"""

from datetime import datetime
from json import dumps, loads
import os

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def process_maps(method: str, output: str):
    """
    Gets a method NDVI | LUMINANCE and loads all the images and
    gets either the ndvi of luminance of an image
    """
    results = []
    base_path = f"data/images/images{method}"
    all_maps = os.listdir(base_path)

    for map_name in tqdm(all_maps):
        download_folders = os.listdir(f"{base_path}/{map_name}/")
        download_folders = [i for i in download_folders if os.path.isdir(
            f"{base_path}/{map_name}/{i}")
            ]

        values = []

        map_coords = []

        for download_folder in download_folders:
            result = compute_download(
                    base_path, map_name, download_folder, map_coords, method
                    )
            values.append(result)

        # Sorting by date
        values = sorted(values, key=lambda x: x[0])
        dates = [v[0] for v in values]
        values = [v[1] for v in values]
        file = plt.figure()
        plt.plot(dates, values, marker='o')
        plt.ylim([-1, 1])
        plt.savefig(f"{base_path}/{map_name}/{map_name}.png")
        plt.close(file)

        result = {
            "nom": map_name,
            method.lower(): values,
            "date": dates,
            "coords": map_coords
        }
        results.append(result)

    with open(output, "w", encoding="utf-8") as file:
        file.write(dumps(results, indent=4, default=str))

def get_date(req):
    """
        Gets the date the photo was taken
    Params:
        req (dict): The content of the request that was sent to sentinelhub
    Returns:
        the date the picture was taken in datetime type
    """

    time_string = req["request"]["payload"]["input"][
            "data"][0]["dataFilter"]["timeRange"]["from"]
    date_iso_format = time_string[:10]

    return datetime.fromisoformat(date_iso_format)

def compute_download(base_path, map_name, download_folder, map_coords, method):
    """
        Calculates NDVI or LUMINANCE data from forest or city data.
        Params:
            base_path (str): the ptah where we can find all the images for all
                the forests or cities
            map_name (str): either the name of the forest, or the name of
                the city
            download_folder (str): the name of the download folder
            map_coords (list): a list of coordinates representing the bounding
                box of a forest
            method (string): it's either NDVI or LUMINANCE 

        Returns:
            A 2 elements array with the date of the request and the mean color
                value of pixels.
            This value corresponds to either the NDVI or LUMINANCE
    """
    result = []
    request = {}

    with open(f"{base_path}/{map_name}/{download_folder}/request.json", "r",
              encoding="utf-8") as file:
        request = loads(file.read())

    result.append(get_date(request))

    if len(map_coords) == 0:
        bbox = request["request"]["payload"]["input"]["bounds"]["bbox"]
        map_coords.append((bbox[0] + bbox[2])/2.0)
        map_coords.append((bbox[1] + bbox[3])/2.0)

    image = plt.imread(
            f"{base_path}/{map_name}/{download_folder}/response.jpg"
            )

    if method == "NDVI":
        image = (image - 255.0 / 2.0) / 255.0

    image_linearized = image.reshape((image.shape[0] * image.shape[1]))
    mean_value = np.mean(image_linearized)

    result.append(mean_value)
    return result


if __name__ == "__main__":
    NDVI_FILE = "data/forests/forests_ndvi.json"
    if not os.path.isfile(NDVI_FILE):
        process_maps("NDVI", NDVI_FILE)

    LUMINANCE_FILE = "data/cities/cities_luminance.json"
    if not os.path.isfile(LUMINANCE_FILE):
        process_maps("LUMINANCE", LUMINANCE_FILE)
