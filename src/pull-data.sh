#!/bin/bash

# cd to file location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

#create and pull data
mkdir -p ../data/forests ../data/cities ../data/images/imagesLUMINANCE ../data/images/imagesNDVI ../maps

# make that parallel (faster)
wget -O ../data/cities/output.zip https://www.insee.fr/fr/statistiques/fichier/6683035/ensemble.zip &
wget -O ../data/forests/FOR_PUBL_FR.json https://www.data.gouv.fr/fr/datasets/r/7b0811ee-9c02-435a-a2e8-440f6a4ffca7 &
wget -O ../data/cities/cities.json https://www.data.gouv.fr/fr/datasets/r/521fe6f9-0f7f-4684-bb3f-7d3d88c581bb &
wget -O ../data/cities/communes.geojson https://github.com/gregoiredavid/france-geojson/raw/master/communes.geojson &

wait # "join threads" (wait for tasks in bg)

# extract data that needs to be extracted
cd ../data/cities/
unzip -o ./output.zip

cd $SCRIPT_DIR
