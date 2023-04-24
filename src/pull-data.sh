#!/bin/bash

# cd to file location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

#create and pull data
mkdir -p ../data/data_cities ../data/data_forest

# make that parallel (faster)
wget -O ../data/data_cities/output.zip https://www.insee.fr/fr/statistiques/fichier/6683035/ensemble.zip
wget -O ../data/data_forest/FOR_PUBL_FR.json https://www.data.gouv.fr/fr/datasets/r/7b0811ee-9c02-435a-a2e8-440f6a4ffca7

wait # "join threads" (wait for tasks in bg)

# extract data that needs to be extracted
cd ../data/data_cities/
unzip -o ./output.zip

cd $SCRIPT_DIR