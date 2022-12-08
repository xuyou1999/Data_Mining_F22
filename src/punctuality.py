import pandas as pd
import numpy as np

# example input variables
route_id = 25
direction_id = 1
date = 20210907
stop = '5407F'
# nbusy_time = [['05:00:00', '07:00:00'], ['07:00:00', '09:00:00'], ['16:00:00', '20:00:00'], ['20:00:00', '25:00:00']]
nbusy_time = [[0,8], [10,12]]

def unix_to_datetime(unix_time):
    return pd.to_datetime(unix_time,unit="ms",origin="unix")

def datetime_to_unix(dt):
    return int(pd.Timestamp.timestamp(pd.Timestamp(dt))*1000)

def get_derived_var(stop, route_id, date, nbusy_time):
    stop_no_letter = ""
    if stop[-1].isalpha():
        stop_no_letter = stop[:-1]
    else:
        stop_no_letter = stop
    # get route short name
    routes = pd.concat([pd.read_csv('../data/gtfs3Sept/routes.csv'), pd.read_csv('../data/gtfs23Sept/routes.csv')])
    route_short_name = routes.loc[routes["route_id"]==route_id,:]["route_short_name"].values[0]
    # Get day of week
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
    # combine time periods
    new_nbusy_time = []
    start = nbusy_time[0][0]
    end = nbusy_time[0][1]
    for i in range(1, len(nbusy_time)):
        if nbusy_time[i][0] == end:
            end = nbusy_time[i][1]
        else:
            new_nbusy_time.append([start, end])
            start = nbusy_time[i][0]
            end = nbusy_time[i][1]
    new_nbusy_time.append([start, end])
    return stop_no_letter, route_short_name, day_of_week, new_nbusy_time

def get_new_nbusy_time_dt(new_nbusy_time, date):
    date_dt = "{}-{}-{}".format(str(date)[:4], str(date)[4:6], str(date)[-2:])
    new_nbusy_time_dt = []
    for i in range(len(new_nbusy_time)):
        new_nbusy_time_dt.append([])
        for j in range(2):
            if new_nbusy_time[i][j] <= '24:00:00':
                new_nbusy_time_dt[i].append(date_dt+" "+new_nbusy_time[i][j])
            else:
                h = int(new_nbusy_time[i][j][:2]) - 24
                h = str(h)
                if len(h) == 1:
                    h = "0"+h
                new_nbusy_time_dt[i].append((pd.to_datetime(date_dt, format='%Y-%m-%d')+pd.Timedelta(days=1)).strftime("%Y-%m-%d")+" "+(h+new_nbusy_time[i][j][2:]))
    return new_nbusy_time_dt, date_dt

def schedule_helper(route_id, direction_id, date, day_of_week, stop, new_nbusy_time):
    # load data
    if date <= 20210919:
        trips = pd.read_csv('../data/gtfs3Sept/trips.csv')
        calendar = pd.read_csv('../data/gtfs3Sept/calendar.csv')
        stop_times = pd.read_csv('../data/gtfs3Sept/stop_times.csv')
    else:
        trips = pd.read_csv('../data/gtfs23Sept/trips.csv')
        calendar = pd.read_csv('../data/gtfs23Sept/calendar.csv')
        stop_times = pd.read_csv('../data/gtfs23Sept/stop_times.csv')
    # trips
    trips_line = trips.loc[trips['route_id']==route_id,:]
    trip_line_head = trips_line.loc[trips_line['direction_id']==direction_id,:]
    # calendar
    calendar_week = calendar.loc[((calendar['start_date']<=date) & (calendar['end_date']>=date)),:]
    calendar_week_day = calendar_week.loc[calendar_week[day_of_week]==1,:]
    trip_line_date_head = pd.merge(left=trip_line_head, right=calendar_week_day, on='service_id', how='inner').loc[:,['route_id','service_id','trip_id']]
    # stop_times
    time_line_date_head = pd.merge(left=trip_line_date_head, right=stop_times, on='trip_id')
    time_line_date_head_stop = time_line_date_head.loc[time_line_date_head['stop_id']==stop,:]
    time_line_date_head_stop = time_line_date_head_stop.sort_values('arrival_time')
    # transform index to time
    for i in range(len(new_nbusy_time)):
        for j in range(2):
            new_nbusy_time[i][j] = time_line_date_head_stop['arrival_time'].values[new_nbusy_time[i][j]]
    return time_line_date_head_stop, new_nbusy_time

def schedule(route_id, direction_id, date, day_of_week, stop, new_nbusy_time):
    time_line_date_head_stop, new_nbusy_time = schedule_helper(route_id, direction_id, date, day_of_week, stop, new_nbusy_time)
    select = (time_line_date_head_stop['arrival_time']>=new_nbusy_time[0][0]) & (time_line_date_head_stop['arrival_time']<=new_nbusy_time[0][1])
    for i in range(len(new_nbusy_time)):
        select = select | ((time_line_date_head_stop['arrival_time']>=new_nbusy_time[i][0]) & (time_line_date_head_stop['arrival_time']<=new_nbusy_time[i][1]))
    time_line_date_head_stop_nbusy = time_line_date_head_stop.loc[select,:]
    return (time_line_date_head_stop_nbusy, new_nbusy_time)

def actural_helper(route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt):
    actural_time = pd.concat([pd.read_csv('../data/vehiclePosition01.csv'),pd.read_csv('../data/vehiclePosition02.csv'),pd.read_csv('../data/vehiclePosition03.csv'),pd.read_csv('../data/vehiclePosition04.csv'),pd.read_csv('../data/vehiclePosition05.csv'),pd.read_csv('../data/vehiclePosition06.csv'),pd.read_csv('../data/vehiclePosition07.csv'),pd.read_csv('../data/vehiclePosition08.csv'),pd.read_csv('../data/vehiclePosition09.csv'),pd.read_csv('../data/vehiclePosition10.csv'),pd.read_csv('../data/vehiclePosition11.csv'),pd.read_csv('../data/vehiclePosition12.csv'),pd.read_csv('../data/vehiclePosition13.csv')])
    actural_time_line = actural_time.loc[actural_time['LineID']==int(route_short_name),:]
    actural_time_line_point = actural_time_line.loc[actural_time_line['PointID']==int(stop_no_letter),:]
    actural_time_line_point['Time'] = actural_time_line_point['Time'].apply(unix_to_datetime)
    actural_time_line_point_date = actural_time_line_point.loc[actural_time_line_point['Time'].dt.date == pd.to_datetime(date_dt).date(),:]
    actural_time_line_point_date['Time'] = (actural_time_line_point_date['Time'] + pd.Timedelta('02:00:00'))
    actural_time_line_point_date_arrive = actural_time_line_point_date.loc[actural_time_line_point_date['DistanceFromPoint']<=200,:]
    select_list = [True]
    for i in range(1, len(actural_time_line_point_date_arrive)):
        if (actural_time_line_point_date_arrive.iloc[i,0] - actural_time_line_point_date_arrive.iloc[i-1,0] <= pd.Timedelta('00:00:45')) and (actural_time_line_point_date_arrive.iloc[i,0] - actural_time_line_point_date_arrive.iloc[i-1,0] >= pd.Timedelta('00:00:15')):
            select_list.append(False)
        else:
            select_list.append(True)
    actural_time_line_point_date_arrive_noduplicate = actural_time_line_point_date_arrive.loc[select_list,:]
    select_list = [True]
    for i in range(1, len(actural_time_line_point_date_arrive_noduplicate)):
        if (actural_time_line_point_date_arrive_noduplicate.iloc[i,0] - actural_time_line_point_date_arrive_noduplicate.iloc[i-1,0] <= pd.Timedelta('00:00:45')) and (actural_time_line_point_date_arrive_noduplicate.iloc[i,0] - actural_time_line_point_date_arrive_noduplicate.iloc[i-1,0] >= pd.Timedelta('00:00:15')):
            select_list.append(False)
        else:
            select_list.append(True)
    actural_time_line_point_date_arrive_noduplicate = actural_time_line_point_date_arrive_noduplicate.loc[select_list,:]
    return actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt

def actural(route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt):
    actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt = actural_helper(route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt)
    select = (actural_time_line_point_date_arrive_noduplicate['Time']>=pd.to_datetime(new_nbusy_time_dt[0][0])) & (actural_time_line_point_date_arrive_noduplicate['Time']<pd.to_datetime(new_nbusy_time_dt[0][1]))
    for i in range(len(new_nbusy_time_dt)):
        select = select | ((actural_time_line_point_date_arrive_noduplicate['Time']>=pd.to_datetime(new_nbusy_time_dt[i][0])) & (actural_time_line_point_date_arrive_noduplicate['Time']<pd.to_datetime(new_nbusy_time_dt[i][1])))
    actural_time_line_point_date_arrive_noduplicate_nbusy = actural_time_line_point_date_arrive_noduplicate.loc[select,:]
    return actural_time_line_point_date_arrive_noduplicate_nbusy

def punctuality(time_line_date_head_stop_nbusy, actural_time_line_point_date_arrive_noduplicate_nbusy, date_dt):
    on_time = 0
    time_line_date_head_stop_nbusy['arrival_time'].apply(pd.to_timedelta)
    actural_time_line_point_date_arrive_noduplicate_nbusy['Time'] - pd.Timestamp(date_dt+' 00:00:00')
    for t in time_line_date_head_stop_nbusy['arrival_time'].apply(pd.to_timedelta):
        ot = False
        for at_i in range(actural_time_line_point_date_arrive_noduplicate_nbusy.shape[0]):
            at = actural_time_line_point_date_arrive_noduplicate_nbusy['Time'].iloc[at_i] - pd.Timestamp(date_dt+' 00:00:00')
            t_dif = t - at
            if actural_time_line_point_date_arrive_noduplicate_nbusy["DistanceFromPoint"].iloc[at_i] != 0:
                if t_dif <= pd.Timedelta('00:00:45') and t_dif >= pd.Timedelta('-00:00:75'):
                    ot = True
            else:
                if t_dif <= pd.Timedelta('00:01:00') and t_dif >= pd.Timedelta('-00:01:00'):
                    ot = True
        if ot == True:
            on_time+=1
    on_time_rate = on_time/len(time_line_date_head_stop_nbusy['arrival_time'])
    return on_time_rate
    

def main(route_id, direction_id, date, stop, nbusy_time):
    stop_no_letter, route_short_name, day_of_week, new_nbusy_time = get_derived_var(stop, route_id, date, nbusy_time)
    time_line_date_head_stop_nbusy, new_nbusy_time = schedule(route_id, direction_id, date, day_of_week, stop, new_nbusy_time)
    new_nbusy_time_dt, date_dt = get_new_nbusy_time_dt(new_nbusy_time, date)
    actural_time_line_point_date_arrive_noduplicate_nbusy = actural(route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt)
    on_time_rate = punctuality(time_line_date_head_stop_nbusy, actural_time_line_point_date_arrive_noduplicate_nbusy, date_dt)
    return on_time_rate

if __name__ == "__main__":
    print(main(route_id, direction_id, date, stop, nbusy_time))
