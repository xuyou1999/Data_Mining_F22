import geopandas as gp
import pandas as pd

stop_data = gp.read_file("2109_STIB_MIVB_Network/ACTU_STOPS.shp")
line_data = gp.read_file("2109_STIB_MIVB_Network/ACTU_LINES.shp")
distance_df = pd.DataFrame({})
for line_name in stop_data['Code_Ligne'].unique():
    for variante in [1, 2]:
        # print(line_name)
        # print(stop_data[stop_data['Code_Ligne']==line_name])
        previous_stop_id, previous_stop_name, previous_stop_geom = None, None, None
        line = line_data.loc[(line_data['LIGNE'] == line_name) & line_data['VARIANTE'] == variante].iterrows()

        line = list(line)
        if not line: continue
        print(line)
        line = line[0][1]
        line_geometry = line['geometry']
        line_points = line_geometry.coords
        for stop in stop_data.loc[(stop_data['Code_Ligne']==line_name) & (stop_data['Variante'] == variante)].sort_values('succession').iterrows():
            # get the LineString geometry of the line through the line code
            stop = stop[1]
            stop_id, stop_name, mode, geometry = stop['stop_id'], stop['alpha_fr'], stop['mode'], stop['geometry']
            if previous_stop_id:
                previous_proj = line_geometry.project(previous_stop_geom)
                current_proj = line_geometry.project(geometry)
                distance = current_proj - previous_proj
                distance_df = distance_df.append({'line_name': line_name, 'start_stop_id':previous_stop_id, 'end_stop_id':stop_id, 'start_stop_name': previous_stop_name, 'end_stop_name': stop_name, 'mode':mode, 'distance':distance}, ignore_index=True)
            previous_stop_id, previous_stop_name, previous_stop_geom = stop_id, stop_name, geometry

print(distance_df)
distance_df.to_csv("distance.csv")
