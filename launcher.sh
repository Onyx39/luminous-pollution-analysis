#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

#bash src/pull-data.sh
#source venv/bin/activate


mkdir logs

python3 -m src.map_creation.process_forest_dataset | tee > logs/process_forest_dataset.log &
python3 -m src.map_creation.process_cities | tee > logs/process_cities.log &
wait

python3 -m src.ndvi_luminance.download_city_images | tee > logs/download_city_images.log & 
python3 -m src.ndvi_luminance.download_forest_images | tee > logs/download_forest_images.log & 
wait 

python3 -m src.ndvi_luminance.process_maps
python3 -m src.map_creation.full_map_creation


