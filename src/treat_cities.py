import json
import pandas as pd

all_departments = ["74", "39"]
data = {}
with open("../data/cities_json/cities.json") as file:
    data = json.load(file)

cities = data["cities"]
cities_dataframe = pd.DataFrame(cities)
cities_dataframe = cities_dataframe.drop(columns=["insee_code", "city_code", "department_name", "region_name", "region_geojson_name"])
cities_filter = cities_dataframe["department_number"].isin(all_departments)
cities_dataframe = cities_dataframe[cities_filter]
output_json = json.loads(cities_dataframe.to_json(orient="records"))

with open("../data/cities_json/cities_output.json", "w") as write_file:
    json.dump(output_json, write_file, indent=4)