import os 
from json import loads, dumps
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

all_forests = os.listdir("imagesNDVI")
results = []

for forest_name in tqdm(all_forests):
    downloads = os.listdir(f"imagesNDVI/{forest_name}/")
    downloads = [i for i in downloads if os.path.isdir(f"imagesNDVI/{forest_name}/{i}" )]

    values = []

    forest_coords = []

    for download in downloads:
        result = []
        request = {}
        
        with open(f"imagesNDVI/{forest_name}/{download}/request.json") as f : 
            request = loads(f.read())
        time_string = request["request"]["payload"]["input"]["data"][0]["dataFilter"]["timeRange"]["from"]
        date_iso_format = time_string[:10] 
        date = datetime.fromisoformat(date_iso_format)
        result.append(date)

        if len(forest_coords) == 0:
            bbox = request["request"]["payload"]["input"]["bounds"]["bbox"]
            forest_coords.append((bbox[0] + bbox[2])/2.0)
            forest_coords.append((bbox[1] + bbox[3])/2.0)

        ndvi_image = plt.imread(f"imagesNDVI/{forest_name}/{download}/response.jpg")
        ndvi_image = (ndvi_image - 255.0 / 2.0)  / 255.0 
        ndvi_image_linearized = ndvi_image.reshape((ndvi_image.shape[0] * ndvi_image.shape[1]))
        mean_ndvi = np.mean(ndvi_image)

        result.append(mean_ndvi)
        values.append(result)

    values = sorted(values, key=lambda x: x[0])
    dates = [v[0] for v in values]
    ndvis = [v[1] for v in values]
    f = plt.figure()
    plt.plot(dates, ndvis, marker='o')
    plt.ylim([-1, 1])
    plt.savefig(f"imagesNDVI/{forest_name}/{forest_name}.png")
    plt.close(f)

    result = {
        "nom" : forest_name,
        "ndvi" : ndvis,
        "date" : dates, 
        "coords" : forest_coords
    }
    results.append(result)

with open("forests_ndvi.json", "w", encoding="utf-8") as f : 
    f.write(dumps(results, indent=4, default=str))


