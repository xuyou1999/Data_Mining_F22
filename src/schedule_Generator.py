import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
pd.options.display.max_rows = 9999
from IPython.display import display

def timeGrouper(stop_id,trip_id):
    stop_times = pd.read_csv("../data/gtfs3Sept/stop_times.csv")
    # stop_times.head()
    stop_times = stop_times.loc[stop_times['stop_id'] == stop_id	].sort_values(by='arrival_time',ascending = True)
    stop_times = stop_times[stop_times['trip_id'].astype(str).str.contains(trip_id)]
    # stop_times
    #This will only deal with the time which is less than 24h. For excess part, we need to count separately
    stop_times['arrival_time'] = pd.to_datetime(stop_times['arrival_time'], errors='coerce')
    stop_times
    time_group = stop_times.groupby(stop_times['arrival_time'].dt.hour).size().reset_index(name='count')
    time_group
    #Here we count for time more than 24h:
    excess_part = stop_times['departure_time']
    excess_part
    # for i in myDuration:
    #     print(i)
    count_24 = 0
    count_25 = 0
    for i in [x for x in excess_part.str.split(":")]:
        if i[0]==('24'):
            count_24 += 1
        if i[0]==('25'):
            count_25 += 1

    time_group = time_group.append({'arrival_time':24,'count':count_24},ignore_index = True)
    time_group = time_group.append({'arrival_time':25,'count':count_25},ignore_index = True)
    
    return time_group

def schedule_gnr(route_short_name,stop_name):
    routes = pd.read_csv("../data/gtfs3Sept/routes.csv")
    route_id = routes.loc[routes['route_short_name']==route_short_name] ##route_short_name is a string
    route_id = route_id['route_id'].values[0]
    
    trips = pd.read_csv('../data/gtfs3Sept/trips.csv')
    trips = trips.loc[trips['route_id'] == route_id]

    stop_times = pd.read_csv('../data/gtfs3Sept/stop_times.csv')
    
    s1 = pd.merge(trips,stop_times, how = 'inner', on=['trip_id'])
    
    stops = pd.read_csv('../data/gtfs3Sept/stops.csv')
    stops = stops.loc[stops['stop_name'] == stop_name]
    
    s2 = pd.merge(stops,s1,how = 'inner' , on=['stop_id'])
    
    stop_id_array = s2['stop_id'].drop_duplicates()
    stop_id_1 = stop_id_array.values[0]
    stop_id_2 = stop_id_array.values[1]
    
    
    #没考虑同一个方向但是中途停下的情况！
    headsign1 = s2.loc[s2['stop_id'] == stop_id_1]['trip_headsign'].values[0]
    headsign2 = s2.loc[s2['stop_id'] == stop_id_2]['trip_headsign'].values[0]
    
    
    
    trips_with_headsign1 = trips.loc[trips['trip_headsign']==headsign1]
    service_id_array_1 =  trips_with_headsign1.drop_duplicates(subset=["service_id"],keep='first')
    trips_with_headsign2 = trips.loc[trips['trip_headsign']==headsign2]
    service_id_array_2 =  trips_with_headsign2.drop_duplicates(subset=["service_id"],keep='first')
    
    calendar = pd.read_csv("../data/gtfs3Sept/calendar.csv")
    calendar1 = pd.merge(calendar,service_id_array_1,how='inner',on=['service_id'])

    print(type(stop_id_1))
    
    for i in range(calendar1.shape[0]):
        service_i = str(calendar1['service_id'][i])
        start_date = calendar1['start_date'][i]
        end_date = calendar1['end_date'][i]
        print(f"from {start_date} to {end_date}, the schedule of line{route_short_name} via direction{headsign1} is as follows:")
        display(timeGrouper(stop_id_1,service_i))
#         print('service_i')


    return