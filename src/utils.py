"""
    Has some functions used in other files
"""

def get_bbox_from_geojson(geojson):
    """
        Gets a geojson object and returns a bbox (longitude 1, latitude 1, longitude 2, latitude 2)
    """
    # Initialize the min and max coordinates
    minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')

    # Loop over the features to find the minimum and maximum coordinates
    if geojson.get('geometry', {}).get('type') == 'Polygon':
        coords = geojson['geometry']['coordinates'][0]
        for coord in coords:
            if coord[0] < minx:
                minx = coord[0]
            if coord[1] < miny:
                miny = coord[1]
            if coord[0] > maxx:
                maxx = coord[0]
            if coord[1] > maxy:
                maxy = coord[1]

    return minx, miny, maxx, maxy
