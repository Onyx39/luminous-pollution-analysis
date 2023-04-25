import os
from json import loads, dumps
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def treat_images(method:str, output:str):
    """ Gets a method NDVI | LUMINANCE and loads all the images and 
        gets either the ndvi of luminance of an image
    """
    results = []
    all_maps = os.listdir(f"data/images/images{method}")

    for map_name in tqdm(all_maps):
        downloads = os.listdir(f"data/images/images{method}/{map_name}/")
        downloads = [i for i in downloads if os.path.isdir(f"data/images/images{method}/{map_name}/{i}")]

        values = []

        map_coords = []

        for download in downloads:
            result = []
            request = {}

            with open(f"data/images/images{method}/{map_name}/{download}/request.json", "r", encoding="utf-8") as file :
                request = loads(file.read())
            time_string = request["request"]["payload"]["input"]["data"][0]["dataFilter"]["timeRange"]["from"]
            date_iso_format = time_string[:10]
            date = datetime.fromisoformat(date_iso_format)
            result.append(date)

            if len(map_coords) == 0:
                bbox = request["request"]["payload"]["input"]["bounds"]["bbox"]
                map_coords.append((bbox[0] + bbox[2])/2.0)
                map_coords.append((bbox[1] + bbox[3])/2.0)

            image = plt.imread(f"data/images/images{method}/{map_name}/{download}/response.jpg")

            if method == "NDVI":
                image = (image - 255.0 / 2.0)  / 255.0
            elif method == "LUMINANCE":
                red, green, blue = image[:, :, 0], image[:, :, 1], image[:, :, 2]
                image = 0.299 * red + 0.587 * green + 0.114 * blue

            image_linearized = image.reshape((image.shape[0] * image.shape[1]))
            mean_value = np.mean(image_linearized)

            result.append(mean_value)
            values.append(result)

        values = sorted(values, key=lambda x: x[0])
        dates = [v[0] for v in values]
        vs = [v[1] for v in values]
        file = plt.figure()
        plt.plot(dates, vs, marker='o')
        plt.ylim([-1, 1])
        plt.savefig(f"data/images/images{method}/{map_name}/{map_name}.png")
        plt.close(file)

        result = {
            "nom" : map_name,
            method.lower() : vs,
            "date" : dates, 
            "coords" : map_coords
        }
        results.append(result)
    with open(output, "w", encoding="utf-8") as file :
        file.write(dumps(results, indent=4, default=str))


if __name__ == "__main__":
    #treat_images("NDVI", "data/forests/forests_ndvi.json")
    treat_images("LUMINANCE", "data/cities/cities_luminance.json")
