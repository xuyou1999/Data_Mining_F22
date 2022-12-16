from punctuality import *
from regularity import *
import ast
import time
# example input variables
route_id = 65
direction_id = 0
date = 20210909
stop = '3510B'
# nbusy_time = [['05:00:00', '07:00:00'], ['07:00:00', '09:00:00'], ['16:00:00', '20:00:00'], ['20:00:00', '25:00:00']]
nbusy_time = []

def calc(trips, calendar, stop_times, actural_time):
    # err_file = pd.read_csv('../result/error_pun_reg_3.txt')
    input_data = pd.read_csv("../result/punc_input_table3.csv")
    output_df = pd.DataFrame(columns=['org_row', 'route_id', 'direction_id', 'date', 'stop_id', 'on_time_rate', 'schedule_waiting_time', 'actual_waiting_time', 'excess_waiting_time', 'weighted_excess', 'a_devided_s'])
    count = 0
    file_number = 0
    for i in range(0, len(input_data)):
    # for i in range(30000, 30020):
    # for j in range(0, len(err_file)):
        # i = err_file.iloc[j,0]
        start = time.time()
        print(i)
        # print(input_data.iloc[i,:])
        org_row = int(input_data.iloc[i,0])
        route_id = int(input_data.iloc[i,1])
        direction_id = int(input_data.iloc[i,2])
        date = int(input_data.iloc[i,3])
        if date <= 20210906 or date >= 20210921:
            continue
        stop = str(input_data.iloc[i,4])
        nbusy_time = input_data.iloc[i,5]
        nbusy_time = ast.literal_eval(nbusy_time)
        try:
            stop_no_letter, route_short_name, day_of_week, new_nbusy_time = get_derived_var(stop, route_id, date, nbusy_time, 3)
            time_line_date_head_stop, new_nbusy_time = schedule_helper(trips, calendar, stop_times, route_id, direction_id, date, day_of_week, stop, new_nbusy_time)
            time_line_date_head_stop_nbusy, new_nbusy_time, time_line_date_head_stop_busy = schedule(time_line_date_head_stop, new_nbusy_time)
            new_nbusy_time_dt, date_dt = get_new_nbusy_time_dt(new_nbusy_time, date)
            actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt = actural_helper(actural_time, route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt)
            if len(actural_time_line_point_date_arrive_noduplicate) == 0:
                continue
            actural_time_line_point_date_arrive_noduplicate_nbusy, actural_time_line_point_date_arrive_noduplicate_busy = actural(actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt)
            on_time_rate = punctuality(time_line_date_head_stop_nbusy, actural_time_line_point_date_arrive_noduplicate_nbusy, date_dt)
            punc_time = time.time()
            if len(time_line_date_head_stop_busy) == 0 or len(actural_time_line_point_date_arrive_noduplicate_busy) == 0:
                regularity_list = {'schedule_waiting_time': [], 'actual_waiting_time': [], 'excess_waiting_time': []}
                weighted_excess = np.nan
            else:
                regularity_list, weighted_excess = regularity(time_line_date_head_stop,time_line_date_head_stop_nbusy,time_line_date_head_stop_busy,
                                    actural_time_line_point_date_arrive_noduplicate,actural_time_line_point_date_arrive_noduplicate_nbusy,
                                    actural_time_line_point_date_arrive_noduplicate_busy)
            a_devided_s = len(actural_time_line_point_date_arrive_noduplicate)/len(time_line_date_head_stop)
            reg_time = time.time()
            # print(punc_time-start, reg_time-punc_time)
            # print(on_time_rate,regularity_list)
            output_df.loc[len(output_df)] =[org_row, route_id, direction_id, date, stop, on_time_rate, regularity_list['schedule_waiting_time'], regularity_list['actual_waiting_time'], regularity_list['excess_waiting_time'], weighted_excess, a_devided_s]
            count += 1
            print(count)
        except:
            error_f = open('../result/error_pun_reg_3.txt', 'a')
            # error_f = open('../result/error_pun_reg_3_new.txt', 'a')
            error_f.write('{}, {}, {}, {}, {}, {} \n'.format(i, org_row, route_id, direction_id, date, stop))
            error_f.close()
        if count >= 1000:
            output_df.to_csv("../result/output_sept3_{}.csv".format(file_number), index=False)
            file_number += 1
            count = 0
            output_df = pd.DataFrame(columns=['org_row', 'route_id', 'direction_id', 'date', 'stop_id', 'on_time_rate', 'schedule_waiting_time', 'actual_waiting_time', 'excess_waiting_time', 'weighted_excess', 'a_devided_s'])
    output_df.to_csv("../result/output_sept3_{}.csv".format(file_number), index=False)

def test(trips, calendar, stop_times, actural_time):
    stop_no_letter, route_short_name, day_of_week, new_nbusy_time = get_derived_var(stop, route_id, date, nbusy_time, 3)
    # print(new_nbusy_time)
    time_line_date_head_stop, new_nbusy_time = schedule_helper(trips, calendar, stop_times, route_id, direction_id, date, day_of_week, stop, new_nbusy_time)
    time_line_date_head_stop_nbusy, new_nbusy_time, time_line_date_head_stop_busy = schedule(time_line_date_head_stop, new_nbusy_time)
    new_nbusy_time_dt, date_dt = get_new_nbusy_time_dt(new_nbusy_time, date)
    actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt = actural_helper(actural_time, route_short_name, stop_no_letter, date_dt, new_nbusy_time_dt)
    actural_time_line_point_date_arrive_noduplicate_nbusy, actural_time_line_point_date_arrive_noduplicate_busy = actural(actural_time_line_point_date_arrive_noduplicate, new_nbusy_time_dt)
    on_time_rate = punctuality(time_line_date_head_stop_nbusy, actural_time_line_point_date_arrive_noduplicate_nbusy, date_dt)
    regularity_list, weighted_excess = regularity(time_line_date_head_stop,time_line_date_head_stop_nbusy,time_line_date_head_stop_busy,
                    actural_time_line_point_date_arrive_noduplicate,actural_time_line_point_date_arrive_noduplicate_nbusy,
                    actural_time_line_point_date_arrive_noduplicate_busy)
    print(actural_time_line_point_date_arrive_noduplicate_busy.iloc[24:30,:])
    print(on_time_rate,regularity_list)
    print(weighted_excess)
    # print(len(time_line_date_head_stop))
    # print(len(actural_time_line_point_date_arrive_noduplicate))

def main():
    trips, calendar, stop_times, actural_time = load_data(20210917)
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