import json

df = open("luminous-pollution-analysis/data/ville_json/cities.json")
data = json.load(df)


infos_villes = {"villes":[]}
for city in data["cities"]:
    ##print(city["city_code"])
    ##print(city["latitude"])
    ##print(city["longitude"])
    if city["latitude"] != "" and city["latitude"] != "":
        infos_villes["villes"].append([city["city_code"], float(city["latitude"]), float(city["longitude"])])
    ##ville["infos"] = [city["city_code"], city["latitude"], city["longitude"]]


json_object = json.dumps(infos_villes, indent = 4) 

with open("luminous-pollution-analysis/data/ville_json/villes.json", "w") as write_file:
    json.dump(infos_villes, write_file, indent=4)