import pandas as pd
import numpy as np
from punctuality import unix_to_datetime,datetime_to_unix,get_derived_var,get_new_nbusy_time_dt,schedule,actural
from Datetime_Calculator import datetime_calculator

#route_id = 25
#trip_headsign = 'BOONDAEL GARE'
#date = 20210907
#stop = '5407F'



#[[0,8], [10,12], [15,16]], 18
def calculate_supplement(nbusy_time, last_number):
    busy_time = []
    for i,element in enumerate(nbusy_time):
        if i == 0:
            if element[0] !=0:
                busy_time.append([0,element[0]])
            else:
                continue
        elif i>0 and i<len(nbusy_time)-1:
            busy_time.append([nbusy_time[i-1][1],nbusy_time[i][0]])
        else:
            busy_time.append([nbusy_time[i-1][1],nbusy_time[i][0]])
            if last_number != nbusy_time[i][1]:
                busy_time.append([nbusy_time[i][1],last_number])
    
    return busy_time


#[[8, 10], [12, 15], [16, 18]]
    
def regularity(stop, route_id, date, trip_headsign, nbusy_time,last_number):
    busy_time = calculate_supplement(nbusy_time, last_number)
    stop_no_letter, route_short_name, day_of_week, new_busy_time = get_derived_var(stop, route_id, date, busy_time)
    time_line_date_head_stop_busy, new_busy_time = schedule(route_id, trip_headsign, date, day_of_week, stop, new_busy_time)
    new_busy_time_dt, date_dt = get_new_nbusy_time_dt(new_busy_time, date)
    actural_time_line_point_date_arrive_noduplicate_busy = actural(route_short_name, stop_no_letter, date_dt, new_busy_time_dt)
    
    schedule_time = time_line_date_head_stop_busy.reset_index()["arrival_time"]
    actural_time = actural_time_line_point_date_arrive_noduplicate_busy.reset_index()["Time"]
    #in order
    schedule_waiting_time = []
    position_indicator = 0
    for item in busy_time:
        number_of_element_in_interval = item[1]-item[0]+1
        df = list(schedule_time.iloc[position_indicator:position_indicator + number_of_element_in_interval].values)
        schedule_waiting_time.append(df)
        position_indicator += number_of_element_in_interval
        
        
    actual_waiting_time = []
    #Time interval
    for j,lst in enumerate(new_busy_time_dt):
        interval = []
        for value in list(actural_time.apply(datetime_to_unix).values):
        
            if value >= datetime_to_unix(lst[0]) and value <=datetime_to_unix(lst[1]):
                interval.append(unix_to_datetime(value))
        actual_waiting_time.append(interval)
                
    
    
    
    
    
    
    
    
    
    return schedule_waiting_time,actual_waiting_time
















