import json
import time
import geopandas as gp
import pandas as pd
from tqdm import tqdm
import os
import csv
stop_data = gp.read_file("2109_STIB_MIVB_Network/ACTU_STOPS.shp")
line_data = gp.read_file("2109_STIB_MIVB_Network/ACTU_LINES.shp")
reverse_variante = True
reverse_map = {1:2, 2:1}
if not reverse_variante:
    bus_on_line_rows = open("bus_on_line1204.csv","r").readlines()
    if os.path.exists("vehicle_distance_result.csv"):
        os.remove("vehicle_distance_result.csv")
    result_file = open("vehicle_distance_result.csv", "a+")
else:
    bus_on_line_rows = open("vehicle_distance_rerun.csv", "r").readlines()
    if os.path.exists("vehicle_distance_rerun_result.csv"):
        os.remove("vehicle_distance_rerun_result.csv")
    result_file = open("vehicle_distance_rerun_result.csv", "a+")


result_file.write("time,lineId,directionId,pointId,distanceFromPoint,distance_from_start_point,vehicle_x,vehicle_y\n")


stop_data['stop_id'] = stop_data['stop_id'].str.extract('(\d+)', expand=False).astype(int)


for row_id, row in enumerate(tqdm(bus_on_line_rows)):
    if row_id == 0: continue
    row = row[:-1]
    row = row.split(",")
    if not row: continue
    time, lineId, pointId, directionId, distanceFromPoint, code_ligne, variante = row

    vehicle_distance, vehicle_x, vehicle_y = [""] * 3
    stop_filted = stop_data.loc[(stop_data['stop_id'] == int(pointId)) & (stop_data['Code_Ligne']==code_ligne)]
    for stop in stop_filted.iterrows():
        stop = dict(stop[1])
        # variante = stop['Variante']
        variante = int(variante)
        line = line_data.loc[(line_data['LIGNE']==code_ligne) & (line_data['VARIANTE'] == (variante if not reverse_variante else reverse_map[variante]))].iterrows()
        line = list(line)
        if not line: continue
        line = line[0][1]
        line_geometry = line['geometry']
        stop_distance = line_geometry.project(stop['geometry'])
        vehicle_distance = stop_distance + float(distanceFromPoint)
        vehicle_point = line_geometry.interpolate(vehicle_distance).xy
        vehicle_x, vehicle_y = vehicle_point[0][0], vehicle_point[1][0]

    result_file.write(",".join([str(time),str(lineId),str(directionId),str(pointId),str(distanceFromPoint),str(vehicle_distance),str(vehicle_x),str(vehicle_y)])+"\n")

