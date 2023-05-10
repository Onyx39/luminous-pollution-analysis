# luminous-pollution-analysis

## Installation

It is required to use python3.10 to run this project.

You may create a virtual environnment to run the project:

```sh
python3.10 -m venv /path/to/venv
```

Install dependencies with the requirements file:

```sh
pip install -r requirements.txt
```

## Scripts featured in the project

```sh
src
├── 📁 evalscripts                    SentinelleHub scripts
├── 📁 map_creation
│   ├── cities_map_creation           Display cities on a map
│   ├── cities_processing             Process cities with their boundaries
│   ├── full_map_creation             Display forests boundaries and their NDVI
│   ├── process_cities                Filter cities by county
│   ├── process_forest_dataset        Process governemental forest data
│   └── simple_map_creation           Dispay forests sqares on a map
├── 📁 ndvi_luminance
│   ├── constants                     Load api keys and other constants
│   ├── distance_forest               Compute distance between city and forest
│   ├── download_city_images          Download city images
│   ├── download_forest_images        Download forest images with correct bands
│   └── process_maps                  Compute NDVI and Luminance
├── pull-data                         Pull needed data
└── utils
```

## Data sources

City, Region and County data from www.insee.fr

https://www.insee.fr/fr/statistiques/fichier/6683035/ensemble.zip

Forest data from www.data.gouv.fr

https://www.data.gouv.fr/fr/datasets/r/7b0811ee-9c02-435a-a2e8-440f6a4ffca7

Cities geolocation from www.data.gouv.fr

https://www.data.gouv.fr/fr/datasets/r/521fe6f9-0f7f-4684-bb3f-7d3d88c581bb

Cities boundaries from gregoiredavid on github

https://github.com/gregoiredavid/france-geojson/raw/master/communes.geojson
