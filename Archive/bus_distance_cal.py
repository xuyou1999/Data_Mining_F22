import json
import time
import geopandas as gp
import pandas as pd
from tqdm import tqdm
import os
stop_data = gp.read_file("2109_STIB_MIVB_Network/ACTU_STOPS.shp")
line_data = gp.read_file("2109_STIB_MIVB_Network/ACTU_LINES.shp")
if os.path.exists("vehicle_distance_result.csv"):
    os.remove("vehicle_distance_result.csv")
result_file = open("vehicle_distance_result.csv","a+")
result_file.write("time,lineId,directionId,pointId,distanceFromPoint,distance_from_start_point,vehicle_x,vehicle_y\n")
for file in tqdm(os.listdir("data")):
    with open("data/"+file,'r') as load_f:
        load_dict = json.load(load_f)
        # print(load_dict)
        for data_dict in tqdm(load_dict['data']):
            time_trans = time.localtime(int(data_dict['time']))
            time_str = time.strftime("%Y-%m-%d %H:%M:%S",time_trans)
            line_list = data_dict['Responses']
            for iter in line_list:
                if not iter: continue
                for buses in iter['lines']:
                    lineId = buses['lineId']
                    str_line_id = lineId.rjust(3,'0')
                    if not buses: continue
                    for vehicle in buses['vehiclePositions']:
                        directionId = vehicle['directionId']
                        distanceFromPoint = vehicle['distanceFromPoint']
                        pointId = vehicle['pointId']
                        stop_filted = stop_data.loc[(stop_data['stop_id'] == pointId) & (stop_data['Code_Ligne'].str.contains(str_line_id))]
                        for stop in stop_filted.iterrows():
                            stop = dict(stop[1])
                            variante = stop['Variante']
                            line = line_data.loc[(line_data['LIGNE'].str.contains(str_line_id)) & line_data['VARIANTE'] == variante].iterrows()
                            line = list(line)
                            if not line: continue
                            line = line[0][1]
                            line_geometry = line['geometry']
                            stop_distance = line_geometry.project(stop['geometry'])
                            vehicle_distance = stop_distance + distanceFromPoint
                            vehicle_point = line_geometry.interpolate(vehicle_distance).xy
                            vehicle_x, vehicle_y = vehicle_point[0][0], vehicle_point[1][0]
                            result_file.write(",".join([data_dict['time'],str(lineId),str(directionId),str(pointId),str(distanceFromPoint),str(vehicle_distance),str(vehicle_x),str(vehicle_y)])+"\n")
                        continue

