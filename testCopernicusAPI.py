import os
import logging
import zipfile
from dotenv import load_dotenv
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt


import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

load_dotenv('.env')
logging.basicConfig(filename="event.log", encoding="utf-8", level=logging.DEBUG, filemode="w")

USER = os.environ.get("COPERNICUS_USER")
PASSWORD = os.environ.get("COPERNICUS_PASSWORD")
api = SentinelAPI(USER, PASSWORD, 'https://scihub.copernicus.eu/dhus')
CLOUD_COVERAGE_THRESHOLD = 30

# Loading area to study
studied_area = read_geojson('c.geojson')

footprint = geojson_to_wkt(studied_area)
processing_level = "Level-2A"
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

files_to_extract = ["B04", "B08","B02","B03"]
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


# Define function to calculate NDVI
def ndvi(red_band, nir_band):
    """Calculate NDVI from red and near-infrared bands"""
    np.seterr(divide='ignore', invalid='ignore')
    return (nir_band - red_band) / (nir_band + red_band)

# Define function to read band data
def read_band(band_path):
    """Read band data from file"""
    with rasterio.open(band_path) as src:
        band_data = src.read(1)
    return band_data

# Define paths to red and near-infrared bands
red_band_path = "Haute-Savoie\S2B_MSIL2A_20230305T102829_N0509_R108_T31TGL_20230305T151653.SAFE\GRANULE\L2A_T31TGL_A031308_20230305T103700\IMG_DATA\R10m\T31TGL_20230305T102829_B04_10m.jp2"
nir_band_path = "Haute-Savoie\S2B_MSIL2A_20230305T102829_N0509_R108_T31TGL_20230305T151653.SAFE\GRANULE\L2A_T31TGL_A031308_20230305T103700\IMG_DATA\R10m\T31TGL_20230305T102829_B08_10m.jp2"

blue_path="Haute-Savoie\S2B_MSIL2A_20230305T102829_N0509_R108_T31TGL_20230305T151653.SAFE\GRANULE\L2A_T31TGL_A031308_20230305T103700\IMG_DATA\R10m\T31TGL_20230305T102829_B02_10m.jp2"
green_path="Haute-Savoie\S2B_MSIL2A_20230305T102829_N0509_R108_T31TGL_20230305T151653.SAFE\GRANULE\L2A_T31TGL_A031308_20230305T103700\IMG_DATA\R10m\T31TGL_20230305T102829_B03_10m.jp2"

# Read red and near-infrared bands
red_band = read_band(red_band_path)
nir_band = read_band(nir_band_path)
green_band=read_band(green_path)
blue_band=read_band(blue_path)
# Calculate NDVI
ndvi_band = ndvi(red_band, nir_band)
luminance_data = 0.2126 * red_band + 0.7152 * green_band+ 0.0722 * blue_band
test_data=red_band+green_band+blue_band


# Plot the NDVI image and save it as a PNG file
show(test_data)
show(ndvi_band, cmap='jet', vmin=-1, vmax=1)
show(luminance_data,cmap='jet_r')
