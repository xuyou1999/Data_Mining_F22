import geopandas as gp
import pandas as pd
from shapely.geometry import LineString, Point
data = gp.read_file("2109_STIB_MIVB_Network/ACTU_STOPS.shp")
filted_data = data[data['Code_Ligne']=='071b']
print(data)
geo_m1 = filted_data['geometry'][1749]
geo_m1_1 = filted_data['geometry'][1750]

print(geo_m1)

data.to_csv("2109_STIB_MIVB_Network/ACTU_STOPS.csv")

data = gp.read_file("2109_STIB_MIVB_Network/ACTU_LINES.shp")
filted_data = data[data['LIGNE']=='071b']

geo_m2 = filted_data['geometry'][110]
print(geo_m2)
distance = geo_m2.distance(geo_m1)
print(distance)
geo_m1_proj = geo_m2.project(geo_m1)
print(geo_m1_proj)
geo_m1_1_proj = geo_m2.project(geo_m1_1)
print(geo_m1_1_proj)

data.to_csv("2109_STIB_MIVB_Network/ACTU_LINES.csv")
