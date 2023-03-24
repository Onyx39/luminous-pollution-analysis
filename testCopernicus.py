from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from dotenv import load_dotenv
import os
from collections import OrderedDict

load_dotenv('.env')
USER = os.environ.get("COPERNICUS_USER")
PASSWORD = os.environ.get("COPERNICUS_PASSWORD")

api = SentinelAPI(USER, PASSWORD, 'https://scihub.copernicus.eu/dhus')

# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson('c.geojson'))
# products = api.query(footprint,
#                      date=('20230310', date(2023, 3, 10)),
#                      platformname='Sentinel-2', 
#                      )

# # convert to Pandas DataFrame
# products_df = api.to_dataframe(products)

# # sort and limit to first 5 sorted products
# # products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
# products_df_sorted = products_df
# products_df_sorted = products_df_sorted.head(1)

# # download sorted and reduced products
# api.download_all(products_df_sorted.index)
# # print(products_df_sorted.index[1])

product_type = 'S2MSI1C'
bands = ["B04", "B08"]

query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI2A',
        'date': ('NOW-14DAYS', 'NOW')}

products = api.query(footprint, date=('NOW-14DAYS', 'NOW'), platformname='Sentinel-2', producttype=product_type)
products_df = api.to_dataframe(products)
products_sorted = products_df.sort_values(["cloudcoverpercentage"], ascending=[True])

print(products_sorted.head(1))


# api.download_all(products)