import pandas as pd
import numpy as np
from punctuality import *
from Datetime_Calculator import datetime_calculator

#route_id = 25
#trip_headsign = 'BOONDAEL GARE'
#date = 20210907
#stop = '5407F'



#[[0,8], [10,12], [15,16]], 18

# def calculate_supplement(nbusy_time, last_number):
#     busy_time = []
#     for i,element in enumerate(nbusy_time):
#         if i == 0:
#             if element[0] !=0:
#                 busy_time.append([0,element[0]])
#             else:
#                 continue
#         elif i>0 and i<len(nbusy_time)-1:
#             busy_time.append([nbusy_time[i-1][1],nbusy_time[i][0]])
#         else:
#             busy_time.append([nbusy_time[i-1][1],nbusy_time[i][0]])
#             if last_number != nbusy_time[i][1]:
#                 busy_time.append([nbusy_time[i][1],last_number])
    
#     return busy_time


# #[[8, 10], [12, 15], [16, 18]]
    
# def regularity_list(stop, route_id, date, direction_id, nbusy_time,last_number):
#     busy_time = calculate_supplement(nbusy_time, last_number)
    
#     stop_no_letter, route_short_name, day_of_week, new_busy_time = get_derived_var(stop, route_id, date, busy_time)
#     time_line_date_head_stop_busy, new_busy_time = schedule(route_id, direction_id, date, day_of_week, stop, new_busy_time)
#     new_busy_time_dt, date_dt = get_new_nbusy_time_dt(new_busy_time, date)
#     actural_time_line_point_date_arrive_noduplicate_busy = actural(route_short_name, stop_no_letter, date_dt, new_busy_time_dt)
    
    
    
#     schedule_time = time_line_date_head_stop_busy.reset_index()["arrival_time"]
#     actural_time = actural_time_line_point_date_arrive_noduplicate_busy.reset_index()["Time"]
#     #in order
#     schedule_waiting_time = []
#     position_indicator = 0
#     for item in busy_time:
#         number_of_element_in_interval = item[1]-item[0]+1
#         df = list(schedule_time.iloc[position_indicator:position_indicator + number_of_element_in_interval].values)
#         schedule_waiting_time.append(df)
#         position_indicator += number_of_element_in_interval
        
        
#     actual_waiting_time = []
#     #Time interval
#     for j,lst in enumerate(new_busy_time_dt):
#         interval = []
#         for value in list(actural_time.apply(datetime_to_unix).values):
        
#             if value >= datetime_to_unix(lst[0]) and value <=datetime_to_unix(lst[1]):
#                 interval.append(unix_to_datetime(value))
#         actual_waiting_time.append(interval)
                
        
    
#     return schedule_waiting_time,actual_waiting_time

#t_change: "2021-09-08 04:59:00.976000"
#t_schedule: "05:08:00"
def unix_to_hour_min_sec(t_change,t_schedule,earliest_date):
    #"08"
    
    #"04"
    t_change = str(t_change["Time"])
    t_change_dayy = int(t_change[8:10])
    t_change_hour = t_change[11:13]
    #print(t_change_hour)
    #"59"
    t_change_min = int(t_change[14:16])
    #"00.976000"
    t_change_seconds = float(t_change[17:23])
    #"05"
    t_schedule_hour = t_schedule[0:2]
    t_change_hour_plus_24 = 0
    #*************************************************Add date condition*******************************
    #Add the next and condition
    if (int(t_change_hour) < int(t_schedule_hour)) and (int(t_change_dayy) > int(earliest_date)):
        t_change_hour_plus_24 = int(t_change_hour)+24
        
        return int(t_change_hour_plus_24) * 3600 + int(t_change_min) * 60 + t_change_seconds
    else:
        return int(t_change_hour) * 3600 + int(t_change_min) * 60 + t_change_seconds
        
        
    
    
    


def regularity(time_line_date_head_stop,time_line_date_head_stop_nbusy,time_line_date_head_stop_busy,
                    actural_time_line_point_date_arrive_noduplicate,actural_time_line_point_date_arrive_noduplicate_nbusy,
                    actural_time_line_point_date_arrive_noduplicate_busy):
    
    
    schedule_total = time_line_date_head_stop[["arrival_time"]]
    schedule_nbusy = time_line_date_head_stop_nbusy[["arrival_time"]]
    schedule_busy = time_line_date_head_stop_busy[["arrival_time"]]
    
    actual_total = actural_time_line_point_date_arrive_noduplicate[["Time"]]
    actual_nbusy = actural_time_line_point_date_arrive_noduplicate_nbusy[["Time"]]
    actual_busy = actural_time_line_point_date_arrive_noduplicate_busy[["Time"]]
    
    
    last_schedule_index = time_line_date_head_stop.shape[0] -1
    busy_index_list = []
    busy_group = time_line_date_head_stop_busy.groupby(time_line_date_head_stop_busy.index.to_series().diff().ne(1).cumsum()).groups
    #print(len(busy_group[1]))
    for value in [list(g) for g in dict(busy_group).values()]:
        expand_lst = []
        if len(value) ==1:
            if value[0] == 0:
                expand_lst.append(value[0])
                expand_lst.append(value[0]+1)
            elif value[0] == last_schedule_index:
                expand_lst.append(value[0]-1)
                expand_lst.append(value[0])
            else:
                expand_lst.append(value[0]-1)
                expand_lst.append(value[0])
                expand_lst.append(value[0]+1)
        else:
            if value[0] == 0 and value[-1] != last_schedule_index:
                for v in value:
                    expand_lst.append(v)
                expand_lst.append(value[-1]+1)
            
            elif value[0] != 0 and value[-1] == last_schedule_index:
                expand_lst.append(value[0]-1)
                for v in value:
                    expand_lst.append(v)
                
            elif value[0] == 0 and value[-1] == last_schedule_index:
                
                for v in value:
                    expand_lst.append(v)
            else:
                expand_lst.append(value[0]-1)
                for v in value:
                    expand_lst.append(v)
                expand_lst.append(value[-1]+1)
                
                
        
        busy_index_list.append(expand_lst)
        
    busy_time_schedule = [schedule_total["arrival_time"].iloc[lst].apply(lambda x: int(x[0:2])*3600+int(x[3:5])*60+int(x[6:7])) for lst  in busy_index_list ]
    #print(busy_time_schedule[0])
    
    #Use this
    print(schedule_total)
    #*************************************************change here********************************************
    earliest_date = str(actural_time_line_point_date_arrive_noduplicate_busy["Time"].iloc[0])[8:10]
    actual_busy_apply = actual_busy.apply(lambda x: unix_to_hour_min_sec(x,schedule_total.iloc[0].values[0],earliest_date),axis = 1)
    #print(actual_busy_apply.head(50))
    print(actual_busy)
    print("Actual_busy_apply:",actual_busy_apply.head(70))
    print("busy_time_schedule:",busy_time_schedule[0].head(70))
    actual_time_inside_schedule = []
    
    for busy_interval in busy_time_schedule:
        actual_time_in_interval = dict()
        start = busy_interval.iloc[0]
        end = busy_interval.iloc[-1]
        for idx,value in actual_busy_apply.iteritems():
            #print(idx)
            if value > start and value < end:
                actual_time_in_interval[idx] = value
        
        actual_time_inside_schedule.append(actual_time_in_interval)
        
        
    print(actual_time_inside_schedule)
         
        
    schedule_waiting_time = []
    for item in busy_time_schedule:
        inter = np.diff(item)/60
        #print(inter)
        final_value = np.sum(np.square(inter)) / (2*(np.sum(inter)))
        schedule_waiting_time.append(final_value)
        
    
    actual_waiting_time = []    
    for i,actual_dict in enumerate(actual_time_inside_schedule):
        if len(actual_dict) == 0:
            correspond_schedule = busy_time_schedule[i]
            
            start = correspond_schedule.values[0]
            end =  correspond_schedule.values[-1]
            
            
            actual_waiting_time.append(np.square(end-start)/2/(end-start)/60)
            
            
            
        elif len(actual_dict) == 1:
            indx = list(actual_dict.keys())[0]
            value_1 = list(actual_dict.values())[0]
            if indx == actual_total.shape[0]-1:
                actual_waiting_time.append(0)
            else:
                search_next =indx +1
                time_unix = actural_time_line_point_date_arrive_noduplicate.iloc[search_next]
                time_in_second = unix_to_hour_min_sec(time_unix,schedule_total.iloc[0].values[0],earliest_date)
                one_value_interval = np.square(time_in_second - value_1)/2/(time_in_second - value_1)/60
                
                actual_waiting_time.append(one_value_interval)
                
            
        
        else:
            time_interval_values = np.diff(list(actual_dict.values()))
            #print(time_interval_values)
            actual_waiting_time.append(np.sum(np.square(time_interval_values)) / (2*(np.sum(time_interval_values)))/60)
            
            
    
    excess_list = [i-j for i,j in zip(actual_waiting_time,schedule_waiting_time)]
        
    
    
    return_dict = dict()
    return_dict["schedule_waiting_time"] = schedule_waiting_time
    return_dict["actual_waiting_time"] = actual_waiting_time
    return_dict["excess_waiting_time"] = excess_list
    
    if len(busy_time_schedule) == 0:
        weighted_excess = np.nan
    else:
        schedule_count = [len(item) for item in busy_time_schedule]
        weighted_excess = np.sum(np.multiply(schedule_count,excess_list))/np.sum(schedule_count)
    
    return return_dict, weighted_excess
    
    
   












