import re
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
pd.options.display.max_rows = 9999
from IPython.display import display
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
from datetime import datetime

import seaborn as sns
from sklearn.neighbors import KNeighborsRegressor
import statistics
import more_itertools as mit
import punctuality


def load_data():
    trips_3 = pd.read_csv('../data/gtfs3Sept/trips.csv')
    calendar_3 = pd.read_csv('../data/gtfs3Sept/calendar.csv')
    stop_times_3 = pd.read_csv('../data/gtfs3Sept/stop_times.csv')
    trips_23 = pd.read_csv('../data/gtfs23Sept/trips.csv')
    calendar_23 = pd.read_csv('../data/gtfs23Sept/calendar.csv')
    stop_times_23 = pd.read_csv('../data/gtfs23Sept/stop_times.csv')
    return trips_3, calendar_3, stop_times_3, trips_23, calendar_23, stop_times_23


def get_day_of_week(date):
    day_of_week = pd.to_datetime(str(date), format='%Y%m%d').dayofweek
    if day_of_week == 0:
        day_of_week = 'monday'
    elif day_of_week == 1:
        day_of_week = 'tuesday'
    elif day_of_week == 2:
        day_of_week = 'wednesday'
    elif day_of_week == 3:
        day_of_week = 'thursday'
    elif day_of_week == 4:
        day_of_week = 'friday'
    elif day_of_week == 5:
        day_of_week = 'saturday'
    elif day_of_week == 6:
        day_of_week = 'sunday'
    return day_of_week

def datetime_calculator(Date1,Date2):
    
    #"H:M:S - H:M:S"
    #Because the data has no minus sign like "-H:M;S", so we can do this.
    #But the calcluation will produce "-H:M:S" if Date1 < Date2
    #So normally there is no mistake.
    pattern1 = r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    if re.match(pattern1, Date1) is not None and re.match(pattern1, Date2) is not None:
        d1_seconds = int(Date1[0:2]) * 3600 + int(Date1[3:5]) * 60 + int(Date1[6:8])
        d2_seconds = int(Date2[0:2]) * 3600 + int(Date2[3:5]) * 60 + int(Date2[6:8])
        interval = d1_seconds - d2_seconds
        sign = np.sign(interval)
        
        hour = str(abs(interval) //3600)
        minutes = str(abs(interval) %3600 // 60)
        seconds = str(abs(interval) - abs(int(hour)) * 3600 - abs(int(minutes)) * 60)
        
        
        if re.match(r"^[0-9]$",hour) is not None:
            hour = "0"+hour
        
        if sign == -1:
            hour = "-"+hour
            
        if re.match(r"^[0-9]$",minutes) is not None:
            minutes = "0"+minutes
        if re.match(r"^[0-9]$",seconds) is not None:
            seconds = "0"+seconds
            
            
        return hour + ":" + minutes + ":" + seconds

def get_join_tables(trips, calendar, stop_times):
    trips.head()
    trip_calendar = pd.merge(trips,calendar, on='service_id', how='inner')
    trip_calendar_stop_times = pd.merge(trip_calendar,stop_times, on='trip_id', how='inner')
    trip_calendar_stop_times_select = trip_calendar_stop_times.loc[:,['route_id', 'direction_id','monday','tuesday','wednesday','thursday','friday','saturday','sunday', 'start_date', 'end_date','stop_id']].drop_duplicates()
    return trip_calendar_stop_times, trip_calendar_stop_times_select


def get_busy_times(stop_times):
    # stop_times = stop_times.loc[stop_times['stop_id'] == stop_id].sort_values(by='arrival_time',ascending = True)
    # stop_times = stop_times[stop_times['trip_id'].astype(str).str.contains(str(trip_id)[-9:])]
    intervals_array = []

    for i in range(len(stop_times['arrival_time'].values)):
        try:
            intervals_array.append(datetime_calculator(stop_times['arrival_time'].values[i+1],stop_times['arrival_time'].values[i]))
        except IndexError:
            intervals_array.append('00:00:00')
    intervals_array = [float(intervals_array[i].split(':')[1])+60*float(intervals_array[i].split(':')[0]) for i in range(len(intervals_array))]

    stop_times['intervals']=intervals_array

    time_integer = float(stop_times['arrival_time'].values[0].split(':')[0])+float(stop_times['arrival_time'].values[0].split(':')[1])/60
    time_integer = [float(stop_times['arrival_time'].values[i].split(':')[0])+float(stop_times['arrival_time'].values[i].split(':')[1])/60 for i in range(len(stop_times['arrival_time'].values))]
    time_integer

    stop_times['time_integer'] = time_integer

    count = 3
    final = []
    # print(intervals_array)
    while count<len(intervals_array):
        # print('len', len(intervals_array))
        # print('count', count)
        first = intervals_array[count-3]
        second = intervals_array[count-2]
        third = intervals_array[count-1]
        fourth = intervals_array[count]
        ls = [first,second,third,fourth]
        std = statistics.stdev(ls)
        
        if std >0.3:
            #jump to four next values
            count += 1
    #         print(count)
        
        else:
            cluster = []
            #zone found:
            cluster.append(count-3)
            cluster.append(count-2)
            cluster.append(count-1)
            cluster.append(count)
            
            extra_num = 0
            #To see if we need to continue exploring
            while std <=0.3:
                extra_num += 1
                cluster.append(count+extra_num)
                try:
                    extra_interval = intervals_array[count+extra_num]
                except:
                    break
                ls.append(extra_interval)
                std = statistics.stdev(ls)
                
            count += 4
            count += extra_num
            
            final.append(cluster)

    other = set(range(len(intervals_array))) - set([i for lst in final for i in lst])
    other = list(other)

    iterable = other
    other = [list(group) for group in mit.consecutive_groups(iterable)]
    # print('other',other)
    #for special cases
    special_case = []
    other_copy = other.copy()
    for i in other:
        if len(i)==1:
            special_case.append(i)
            other_copy.remove(i)
    # print(special_case)

    ##########

    final_group = []
    for i in final:
        final_group.append([i[0],i[-1]])
    for i in other_copy:
        final_group.append([i[0],i[-1]])
    
    for subls in final_group:
        for special in special_case:
            if special[0] == subls[0]-1:
                subls[0]=special[0]
    # print(final_group)

    reg_or_punc = []
    mean = np.median(intervals_array)
    mean
    for i in final_group:
        begin = i[0]
        end = i[1]
        sum = 0
        # print('begin',begin)
        # print('end',end)
        # print('interval', len(intervals_array))
        diff = end - begin
        while begin<end:
            sum += intervals_array[begin]
            begin += 1
        mean_calc = sum/diff
        if mean_calc > mean:
            reg_or_punc.append("Punctual Zone")
        else:
            reg_or_punc.append("Regular Zone")
    
    df = pd.DataFrame(list(zip(final_group,reg_or_punc)))
    # print(df)
    punc_input = df[df[1] == "Punctual Zone"].loc[:,0].sort_values().to_list()
    return punc_input


def main():
    trips_3, calendar_3, stop_times_3, trips_23, calendar_23, stop_times_23 = load_data()
    trip_calendar_stop_times, trip_calendar_stop_times_select = get_join_tables(trips_3, calendar_3, stop_times_3)
    punc_input_table = pd.DataFrame(columns=['org_row','route_id', 'direction_id','date','stop_id', 'punc'])
    count = 0
    file_number = 0
    for i in range(0, len(trip_calendar_stop_times_select)):
    # for i in range(1901, 1950):
        print('i', i)
        route_id = trip_calendar_stop_times_select.iloc[i,0]
        direction_id = trip_calendar_stop_times_select.iloc[i,1]
        for date in range(trip_calendar_stop_times_select.iloc[i,9],trip_calendar_stop_times_select.iloc[i,10]+1):
            if date >= 20210931 and date <= 20211000:
                continue
            day_of_week = get_day_of_week(date)
            if trip_calendar_stop_times_select.iloc[i][day_of_week] == 1:
                stop_id = trip_calendar_stop_times_select.iloc[i,11]
                # print(route_id, direction_id, date, stop_id)
                arrival = trip_calendar_stop_times.loc[trip_calendar_stop_times['route_id'] == route_id]
                arrival = arrival.loc[arrival['direction_id'] == direction_id]
                arrival = arrival.loc[(arrival['start_date'] <= date) & (arrival['end_date'] >= date)]
                arrival = arrival.loc[arrival[day_of_week] == 1]
                # print('arrival', arrival.loc[:,['stop_id','arrival_time']].sort_values(by=['stop_id']).head(400))
                arrival = arrival.loc[arrival['stop_id'] == stop_id]
                arrival = arrival.loc[:,['arrival_time']].sort_values(by=['arrival_time'])
                try:
                    punc_input = get_busy_times(arrival)
                    punc_input_table.loc[len(punc_input_table)] = [i,route_id, direction_id, date, stop_id, punc_input]
                    count += 1
                except:
                    error_f = open('../result/error3.txt', 'a')
                    error_f.write('{}, {}, {}, {}, {} \n'.format(i, route_id, direction_id, date, stop_id))
                    error_f.close()
        if count >= 2000:
            punc_input_table.to_csv('../result/punc_input_table3_{}.csv'.format(file_number))
            file_number += 1
            count = 0
            punc_input_table = pd.DataFrame(columns=['org_row','route_id', 'direction_id','date','stop_id', 'punc'])
    punc_input_table.to_csv('../result/punc_input_table3_{}.csv'.format(file_number))
    return 0

def debug(i):
    trips_3, calendar_3, stop_times_3, trips_23, calendar_23, stop_times_23 = load_data()
    trip_calendar_stop_times, trip_calendar_stop_times_select = get_join_tables(trips_3, calendar_3, stop_times_3)

    print('i', i)
    route_id = trip_calendar_stop_times_select.iloc[i,0]
    direction_id = trip_calendar_stop_times_select.iloc[i,1]
    for date in range(trip_calendar_stop_times_select.iloc[i,9],trip_calendar_stop_times_select.iloc[i,10]+1):
        if date >= 20210931 and date <= 20211000:
            continue
        day_of_week = get_day_of_week(date)
        if trip_calendar_stop_times_select.iloc[i][day_of_week] == 1:
            stop_id = trip_calendar_stop_times_select.iloc[i,11]
            print(route_id, direction_id, date, stop_id)
            arrival = trip_calendar_stop_times.loc[trip_calendar_stop_times['route_id'] == route_id]
            arrival = arrival.loc[arrival['direction_id'] == direction_id]
            arrival = arrival.loc[(arrival['start_date'] <= date) & (arrival['end_date'] >= date)]
            arrival = arrival.loc[arrival[day_of_week] == 1]
            # print('arrival', arrival.loc[:,['stop_id','arrival_time']].sort_values(by=['stop_id']).head(400))
            arrival = arrival.loc[arrival['stop_id'] == stop_id]
            arrival = arrival.loc[:,['arrival_time']].sort_values(by=['arrival_time'])
            print(arrival)
            punc_input = get_busy_times(arrival)
            print(punc_input)
    return 0


if __name__ == '__main__':
    main()
    # debug(21336)