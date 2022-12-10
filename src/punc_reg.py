from punctuality import *
from regularity import *
# example input variables
route_id = 25
direction_id = 1
date = 20210907
stop = '5407F'
# nbusy_time = [['05:00:00', '07:00:00'], ['07:00:00', '09:00:00'], ['16:00:00', '20:00:00'], ['20:00:00', '25:00:00']]
nbusy_time = [[0,8], [10,12]]

def main(route_id, direction_id, date, stop, nbusy_time):
    trips, calendar, stop_times, actural_time = load_data(date)
    stop_no_letter, route_short_name, day_of_week, new_nbusy_time = get_derived_var(stop, route_id, date, nbusy_time)
    time_line_date_head_stop, new_nbusy_time = schedule_helper(trips, calendar, stop_times, route_id, direction_id, date, day_of_week, stop, new_nbusy_time)
    time_line_date_head_stop_nbusy, new_nbusy_time, time_line_date_head_stop_busy = schedule(time_line_date_head_stop, new_nbusy_time)
    new_nbusy_time_dt, date_dt = get_new_nbusy_time_dt(new_nbusy_time, date)
    actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt = actural_helper(actural_time, route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt)
    actural_time_line_point_date_arrive_noduplicate_nbusy, actural_time_line_point_date_arrive_noduplicate_busy = actural(actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt)
    on_time_rate = punctuality(time_line_date_head_stop_nbusy, actural_time_line_point_date_arrive_noduplicate_nbusy, date_dt)
    return on_time_rate

if __name__ == '__main__':
    on_time_rate = main(route_id, direction_id, date, stop, nbusy_time)
    print(on_time_rate)