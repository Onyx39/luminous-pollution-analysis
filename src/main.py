import json 

# WARNING
# Please download the dataset at 
# https://www.data.gouv.fr/fr/datasets/forets-publiques-diffusion-publique-1/
# (the first on the page : FOR_PUBL_FR), put in in data_forest

def get_forest_file () : 
    f = open("../data/data_forest/FOR_PUBL_FR.json")
    data = json.load(f)

    forest_list = []
    polygon_list = []

    for i in data["features"]: 
        forest_list.append([i["properties"]["llib_frt"], i["geometry"]["coordinates"]])
    
    with open('../data/data_forest/forests.json', 'w', encoding='utf-8') as json_file:
        for j in forest_list : 
            point_cardinaux = [j[1][0][0][0], j[1][0][0][0], j[1][0][0][1], j[1][0][0][1]]
            for k in j[1][0] : 
                if k[0] < point_cardinaux[0] :
                    point_cardinaux[0] = k[0]
                if k[0] > point_cardinaux[1] :
                    point_cardinaux[1] = k[0]
                if k[1] < point_cardinaux[2] :
                    point_cardinaux[2] = k[1]
                if k[1] > point_cardinaux[3] :
                    point_cardinaux[3] = k[1]

            polygon = {"type" : "Feature", 
                        "geometry" : {
                            "type" : "Polygon", 
                            "coordinates" : 
                            [
                                [
                                    [point_cardinaux[1], point_cardinaux[3]],
                                    [point_cardinaux[0], point_cardinaux[3]], 
                                    [point_cardinaux[0], point_cardinaux[2]],
                                    [point_cardinaux[1], point_cardinaux[2]]
                                ]
                            ]
                        },
                        "properties" :  {
                            "nom" : j[0]
                        }
                        }
            polygon_list.append(polygon)
        json.dump(polygon_list, json_file,ensure_ascii=False)          

    f.close()

    return True

get_forest_file()

