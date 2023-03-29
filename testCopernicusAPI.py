from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from dotenv import load_dotenv
import os
import logging
import zipfile

# Loading preferences 

load_dotenv('.env')
logging.basicConfig(filename="event.log", encoding="utf-8", level=logging.DEBUG, filemode="w")

USER = os.environ.get("COPERNICUS_USER")
PASSWORD = os.environ.get("COPERNICUS_PASSWORD")
api = SentinelAPI(USER, PASSWORD, 'https://scihub.copernicus.eu/dhus')
CLOUD_COVERAGE_THRESHOLD = 30

# Loading area to study
studied_area = read_geojson('c.geojson')

footprint = geojson_to_wkt(studied_area)
processing_level = "Level-1C"
products = api.query(footprint, date=('NOW-30DAYS', 'NOW'), platformname='Sentinel-2', processinglevel=processing_level)

# Filter per cloud coverage
products = dict(filter(lambda x: x[1]["cloudcoverpercentage"] < CLOUD_COVERAGE_THRESHOLD, products.items()))

# Checking if we need to download all the files
already_downloaded_files = os.listdir("./data/sentinel2_data")
needed_files = [product["title"]+".zip" for product in products.values()]

download_required = False
for file in needed_files:
    if file not in already_downloaded_files:
        download_required = True

if download_required:
    api.download_all(products, directory_path="./data/sentinel2_data")


# Extracting some file of the archive

files_to_extract = ["B04", "B08"]
folder_name = studied_area["properties"]["nom"]

try:
    os.mkdir(folder_name)
except FileExistsError as e:
    logging.error(f'The directory {folder_name} already exists')

for zip_file_path in needed_files : 
    with zipfile.ZipFile("data/sentinel2_data/"+zip_file_path, "r") as zip_file:
        for zf in zip_file.filelist:
            for file_name in files_to_extract:
                if file_name in zf.filename:
                    zip_file.extract(zf.filename, path=folder_name)