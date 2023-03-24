import json 

# WARNING
# Please download the dataset at 
# https://www.data.gouv.fr/fr/datasets/forets-publiques-diffusion-publique-1/
# (the first on the page : FOR_PUBL_FR), put in in data_forest

def quadri (nom_foret) : 
    f = open("data_forest/FOR_PUBL_FR.json")
    data = json.load(f)

    for i in data["features"]: 
        if i["properties"]["llib_frt"] == nom_foret :
            print("Forêt communale d'Annecy-Annecy-Le-Vieux")
            coor = i["geometry"]["coordinates"]
            break
    
    point_cardinaux = [coor[0][0][0][0], coor[0][0][0][0], coor[0][0][0][1], coor[0][0][0][1]]
    for i in coor[0][0] : 
        if i[0] < point_cardinaux[0] :
            point_cardinaux[0] = i[0]
        if i[0] > point_cardinaux[1] :
            point_cardinaux[1] = i[0]
        if i[1] < point_cardinaux[2] :
            point_cardinaux[2] = i[1]
        if i[1] > point_cardinaux[3] :
            point_cardinaux[3] = i[1]
    for i in range(len(point_cardinaux)) :
         point_cardinaux[i] = point_cardinaux[i] - 0.0001
    print(point_cardinaux)

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
                    "nom" : nom_foret
                }
                }
    f.close()
    return polygon

print(quadri("Forêt communale d'Annecy-Annecy-Le-Vieux"))
