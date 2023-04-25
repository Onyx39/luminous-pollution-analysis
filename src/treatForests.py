import os
from json import loads, dumps
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

image_type = "imageLUMINANCE"  # Modifier cette valeur pour "imagesNDVI" ou "imageLUMINANCE"

all_forests = os.listdir(image_type)
results = []

for forest_name in tqdm(all_forests):
    downloads = os.listdir(f"{image_type}/{forest_name}/")
    downloads = [i for i in downloads if os.path.isdir(f"{image_type}/{forest_name}/{i}")]

    values = []

    forest_coords = []

    for download in downloads:
        result = []
        request = {}

        with open(f"{image_type}/{forest_name}/{download}/request.json") as f:
            request = loads(f.read())
        time_string = request["request"]["payload"]["input"]["data"][0]["dataFilter"]["timeRange"]["from"]
        date_iso_format = time_string[:10]
        date = datetime.fromisoformat(date_iso_format)
        result.append(date)

        if len(forest_coords) == 0:
            bbox = request["request"]["payload"]["input"]["bounds"]["bbox"]
            forest_coords.append((bbox[0] + bbox[2]) / 2.0)
            forest_coords.append((bbox[1] + bbox[3]) / 2.0)

        image = plt.imread(f"{image_type}/{forest_name}/{download}/response.jpg")

        if image_type == "imagesNDVI":
            image = (image - 255.0 / 2.0) / 255.0
        elif image_type == "imageLUMINANCE":
            red, green, blue = image[:, :, 0], image[:, :, 1], image[:, :, 2]
            image = 0.299 * red + 0.587 * green + 0.114 * blue

        image_linearized = image.reshape((image.shape[0] * image.shape[1]))
        mean_value = np.mean(image)

        result.append(mean_value)
        values.append(result)

    values = sorted(values, key=lambda x: x[0])
    dates = [v[0] for v in values]
    values = [v[1] for v in values]
    f = plt.figure()
    plt.plot(dates, values, marker='o')
    plt.ylim([-1, 1] if image_type == "imagesNDVI" else [0, 255])
    plt.savefig(f"{image_type}/{forest_name}/{forest_name}.png")
    plt.close(f)

    result = {
        "nom": forest_name,
        "value": values,
        "date": dates,
        "coords": forest_coords
    }
    results.append(result)

with open(f"forests_{image_type.lower()}.json", "w", encoding="utf-8") as f:
    f.write(dumps(results, indent=4, default=str))
