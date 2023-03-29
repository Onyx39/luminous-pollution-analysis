from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from dotenv import load_dotenv
import os
import logging

load_dotenv('.env')
logging.basicConfig(filename="event.log", encoding="utf-8", level=logging.DEBUG, filemode="w")

USER = os.environ.get("COPERNICUS_USER")
PASSWORD = os.environ.get("COPERNICUS_PASSWORD")
api = SentinelAPI(USER, PASSWORD, 'https://scihub.copernicus.eu/dhus')

studied_area = read_geojson('c.geojson')

footprint = geojson_to_wkt(studied_area)

product_type = 'S2MSI1C'
# product_type = 'S2MSI1A'
# product_type = 'S2MSI1B'
processing_level = "Level-1C"

# products = api.query(footprint, date=('NOW-60DAYS', 'NOW'), platformname='Sentinel-2', producttype=product_type)
products = api.query(footprint, date=('NOW-14DAYS', 'NOW'), platformname='Sentinel-2', processinglevel=processing_level)

already_downloaded_files = os.listdir("./data/sentinel2_data")

needed_files = [product["title"]+".zip" for product in products.values()]

download_required = False
for file in needed_files:
    if file not in already_downloaded_files:
        download_required = True

if download_required:
    api.download_all(products, directory_path="./data/sentinel2_data")

# os.mkdir()

files_to_extract = ["B04", "B08"]

# products_df = api.to_dataframe(products)
# print(products_sorted.columns)

# api.download_all(products, directory_path="./data/")