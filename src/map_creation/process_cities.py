"""gen a currated list of cities and their useful props"""
import json

import pandas as pd

from src.utils import load_data

WANTED_DEPARTEMENTS = ["23"]

def process_data (dictionary):
    '''
    Returns a dataframe that only contains the data we want.

        Parameter:
                dictionary (dictionary) : The whole data
        Returns:
                cities_dataframe (dictionary): The cleaned dictionary
    '''
    # Get the cities
    cities_dataframe = pd.DataFrame(dictionary["cities"])

    # Filter by departements
    cities_filter = cities_dataframe["department_number"]\
            .isin(WANTED_DEPARTEMENTS)
    cities_dataframe = cities_dataframe[cities_filter]

    # Remove unusefull columns
    columns=["insee_code", "city_code", "department_name", "region_name", \
            "region_geojson_name"]
    cities_dataframe = cities_dataframe.drop(columns=columns)

    return cities_dataframe


### LOAD THE DATA ###
print("Opening data file...")
data = load_data("data/cities/cities.json")

### PROCESS THE DATA ###
cleaned_dataframe = process_data(data)
output_json = json.loads(cleaned_dataframe.to_json(orient="records"))

### SAVE THE FILE ###
print("Saving file...")
with open("data/cities/cities_output.json", "w", encoding="utf-8")\
        as write_file:
    json.dump(output_json, write_file, indent=4)

print("Completion of execution : OK")
