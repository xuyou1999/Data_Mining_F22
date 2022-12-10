from punctuality import *
from regularity import *
import ast
# example input variables
route_id = 25
direction_id = 1
date = 20210907
stop = '5407F'
# nbusy_time = [['05:00:00', '07:00:00'], ['07:00:00', '09:00:00'], ['16:00:00', '20:00:00'], ['20:00:00', '25:00:00']]
nbusy_time = [[4,8], [15,39], [40,60]]

def calc(trips, calendar, stop_times, actural_time):
    input_data = pd.read_csv("../result/punc_input_table_sept3.csv")
    output_df = pd.DataFrame(columns=['org_row', 'route_id', 'direction_id', 'date', 'stop_id', 'on_time_rate', 'schedule_waiting_time', 'actual_waiting_time', 'excess_waiting_time'])
    i = 0
    for row in input_data.itertuples():
        org_row = int(row.org_row)
        route_id = int(row.route_id)
        direction_id = int(row.direction_id)
        date = int(row.date)
        if date <= 20210905:
            continue
        stop = str(row.stop_id)
        nbusy_time = row.punc
        nbusy_time = ast.literal_eval(nbusy_time)
        stop_no_letter, route_short_name, day_of_week, new_nbusy_time = get_derived_var(stop, route_id, date, nbusy_time)
        # print(new_nbusy_time)
        time_line_date_head_stop, new_nbusy_time = schedule_helper(trips, calendar, stop_times, route_id, direction_id, date, day_of_week, stop, new_nbusy_time)
        time_line_date_head_stop_nbusy, new_nbusy_time, time_line_date_head_stop_busy = schedule(time_line_date_head_stop, new_nbusy_time)
        new_nbusy_time_dt, date_dt = get_new_nbusy_time_dt(new_nbusy_time, date)
        actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt = actural_helper(actural_time, route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt)
        actural_time_line_point_date_arrive_noduplicate_nbusy, actural_time_line_point_date_arrive_noduplicate_busy = actural(actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt)
        on_time_rate = punctuality(time_line_date_head_stop_nbusy, actural_time_line_point_date_arrive_noduplicate_nbusy, date_dt)
        regularity_list = regularity(time_line_date_head_stop,time_line_date_head_stop_nbusy,time_line_date_head_stop_busy,
                            actural_time_line_point_date_arrive_noduplicate,actural_time_line_point_date_arrive_noduplicate_nbusy,
                            actural_time_line_point_date_arrive_noduplicate_busy)
        # print(on_time_rate,regularity_list)
        output_df.loc[len(output_df)] =[org_row, route_id, direction_id, date, stop, on_time_rate, regularity_list['schedule_waiting_time'], regularity_list['actual_waiting_time'], regularity_list['excess_waiting_time']]
        print(i)
        i += 1
    output_df.to_csv("../result/output_sept3.csv", index=False)

def test(trips, calendar, stop_times, actural_time):
    stop_no_letter, route_short_name, day_of_week, new_nbusy_time = get_derived_var(stop, route_id, date, nbusy_time)
    # print(new_nbusy_time)
    time_line_date_head_stop, new_nbusy_time = schedule_helper(trips, calendar, stop_times, route_id, direction_id, date, day_of_week, stop, new_nbusy_time)
    time_line_date_head_stop_nbusy, new_nbusy_time, time_line_date_head_stop_busy = schedule(time_line_date_head_stop, new_nbusy_time)
    new_nbusy_time_dt, date_dt = get_new_nbusy_time_dt(new_nbusy_time, date)
    actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt = actural_helper(actural_time, route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt)
    actural_time_line_point_date_arrive_noduplicate_nbusy, actural_time_line_point_date_arrive_noduplicate_busy = actural(actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt)
    on_time_rate = punctuality(time_line_date_head_stop_nbusy, actural_time_line_point_date_arrive_noduplicate_nbusy, date_dt)
    regularity_list = regularity(time_line_date_head_stop,time_line_date_head_stop_nbusy,time_line_date_head_stop_busy,
                        actural_time_line_point_date_arrive_noduplicate,actural_time_line_point_date_arrive_noduplicate_nbusy,
                        actural_time_line_point_date_arrive_noduplicate_busy)

def main():
    trips, calendar, stop_times, actural_time = load_data(date)
    test(trips, calendar, stop_times, actural_time)
    # calc(trips, calendar, stop_times, actural_time)
    
    # print(time_line_date_head_stop,"\n")
    # print(time_line_date_head_stop_nbusy,"\n")
    # print(time_line_date_head_stop_busy,"\n") 
    # print(actural_time_line_point_date_arrive_noduplicate,"\n")
    # print(actural_time_line_point_date_arrive_noduplicate_nbusy,"\n")
    # print(actural_time_line_point_date_arrive_noduplicate_busy,"\n")
    # return (on_time_rate,regularity_list)
    


if __name__ == '__main__':
    main()