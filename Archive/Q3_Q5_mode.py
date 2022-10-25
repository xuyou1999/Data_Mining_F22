import pandas as pd
from tqdm import tqdm
import numpy as np
train_path = "other_data/aggregate_data_train.csv"
test_path = "other_data/calender_estimate_1219_test_filted.csv"
 # to find the influence of each condition
np.random.seed(2021)
use_random_estimate = False
for my_mode in ["m","b","t"]:
    data_1218 = open(test_path, "r")
    df = pd.read_csv(train_path)
    num_lines = sum(1 for line in open(test_path, "r"))
    error_list = []
    error_list_time = []
    condition_record = [0] * 10
    with data_1218 as f:
        pbar = tqdm(f, total=num_lines)
        for line in pbar:
            line = line[:-1]
            # break
            line = line.replace("\"","")
            trip_id,stop_id,stop_sequence, line_id, mode, is_weekend,is_rain,t_cls,pre_bus_distance,speed,interpolated_arrival_time,calendar_time,how_long_delay_or_ahead, variante = line.split(",")
            if trip_id == "trip_id": continue # skip first line
            if use_random_estimate:
                if np.random.rand() > 0.25: continue
            if not mode == "b": continue
            # if not line_id == "95": continue

            minite_30_times =  np.floor((int(calendar_time[11:13]) *60 + int(calendar_time[14:16]) + int(calendar_time[17:19]) /60.0) / 30)
            t_cls = int(t_cls)
            is_rain = int(is_rain)
            is_weekend = int(is_weekend)
            stop_sequence = int(stop_sequence)
            stop_section = np.floor(int(stop_sequence)/6.0)
            trip_id = int(trip_id)
            variante = int(variante)
            line_id = int(line_id)
            how_long_delay_or_ahead = float(how_long_delay_or_ahead)
            pre_bus_distance = float(pre_bus_distance)
            speed = float(speed)
            time_before = pre_bus_distance/speed
            df1 = df.loc[(df["mode"]==mode) & (df['t_cls']==t_cls) & (df['is_rain']==is_rain) & (df['is_weekend']==is_weekend)]
            while True:
                    # A specific stop and time
                    aggre_delay_df = df1.loc[(df1['minite_30_times'] == minite_30_times) & (df1["line_id"] == line_id) & (
                                df1['variante'] == variante) & (df1['stop_sequence'] == stop_sequence)]
                    if not aggre_delay_df.empty:
                        condition_record[0] += 1
                        break

                    # B specific stop and ambiguous time
                    aggre_delay_df = df1.loc[((df1['minite_30_times'] == minite_30_times)|(df1['minite_30_times'] == minite_30_times-1)|(df1['minite_30_times'] == minite_30_times+1)) & (df1["line_id"] == line_id) & (
                            df1['variante'] == variante) & (df1['stop_sequence'] == stop_sequence)]
                    if not aggre_delay_df.empty:
                        condition_record[1] += 1
                        break

                    # C ambiguous stop and specific time
                    aggre_delay_df = df1.loc[(df1['minite_30_times'] == minite_30_times) & (df1["line_id"] == line_id) & (
                                df1['variante'] == variante) & (
                        (df1['stop_sequence'] == stop_sequence-1)|(df1['stop_sequence'] == stop_sequence)|(df1['stop_sequence'] == stop_sequence+1))]
                    if not aggre_delay_df.empty:
                        condition_record[2] += 1
                        break

                    # D. ambiguous stop and ambiguous time
                    aggre_delay_df = df1.loc[((df1['minite_30_times'] == minite_30_times)|(df1['minite_30_times'] == minite_30_times-1)|(df1['minite_30_times'] == minite_30_times+1)) & (df1["line_id"] == line_id) & (
                            df1['variante'] == variante) & (
                                                     (df1['stop_sequence'] == stop_sequence - 1) | (
                                                         df1['stop_sequence'] == stop_sequence) | (
                                                                 df1['stop_sequence'] == stop_sequence + 1))]
                    if not aggre_delay_df.empty:
                        condition_record[3] += 1
                        break


                    # E. only specific stop
                    aggre_delay_df = df1.loc[
                        (df1['minite_30_times'] == -1) & (df1["line_id"] == line_id) & (df1['variante'] == variante) & (
                                df1['stop_sequence'] == stop_sequence)]
                    if not aggre_delay_df.empty:
                        condition_record[4] += 1
                        break

                    # F. only ambiguous stop
                    aggre_delay_df = df1.loc[
                        (df1['minite_30_times'] == -1) & (df1["line_id"] == line_id) & (df1['variante'] == variante) & (
                        (df1['stop_sequence'] == stop_sequence-1)|(df1['stop_sequence'] == stop_sequence)|(df1['stop_sequence'] == stop_sequence+1))]
                    if not aggre_delay_df.empty:
                        condition_record[5] += 1
                        break

                    # G.1 directed line and specific time
                    aggre_delay_df = df1.loc[(df1['minite_30_times'] == minite_30_times) & (df1["line_id"] == line_id) & (
                                df1['variante'] == variante) & (
                                                     df1['stop_section'] == -1)]
                    if not aggre_delay_df.empty:
                        condition_record[6] += 1
                        break

                    # G.2 directed line and ambiguous time
                    aggre_delay_df = df1.loc[((df1['minite_30_times'] == minite_30_times)|(df1['minite_30_times'] == minite_30_times-1)|(df1['minite_30_times'] == minite_30_times+1)) & (df1["line_id"] == line_id) & (
                                df1['variante'] == variante) & (
                                                     df1['stop_section'] == -1)]
                    if not aggre_delay_df.empty:
                        condition_record[6] += 1
                        break

                    # H.1 only specific time
                    aggre_delay_df = df1.loc[(df1['minite_30_times'] == minite_30_times) & (df1["line_id"] == line_id) & (
                                df1['variante'] == variante) & (
                                                     df1['stop_section'] == -1)]
                    if not aggre_delay_df.empty:
                        condition_record[7] += 1
                        break

                    # H.2 only ambiguous time
                    aggre_delay_df = df1.loc[(df1['minite_30_times'] == minite_30_times) & (df1["line_id"] == line_id) & (
                            df1['variante'] == variante) & (
                                                     df1['stop_section'] == -1)]
                    if not aggre_delay_df.empty:
                        condition_record[7] += 1
                        break

                    # I. only directed line section
                    aggre_delay_df = df1.loc[
                        (df1['minite_30_times'] == -1) & (df1["line_id"] == line_id) & (df1['variante'] == variante) & (
                                df1['stop_section'] == -1)]
                    if not aggre_delay_df.empty:
                        condition_record[8] += 1
                        break

                    # J. the least info section: mode and environment
                    aggre_delay_df = df1.loc[
                        (df1['minite_30_times'] == -1) & (df1["line_id"] == -1) & (df1['variante'] == -1) & (
                                df1['stop_section'] == -1)]
                    condition_record[9] += 1
                    break

            if aggre_delay_df.empty:
                # print(aggre_delay_df)
                # miss_line.append(miss_line)
                continue
            delay = np.average(list(aggre_delay_df['avg_delay']))
            error_list.append(np.abs(delay-how_long_delay_or_ahead))
            aggre_speed = list(aggre_delay_df['avg_speed'])[0]
            aggre_time = pre_bus_distance / aggre_speed
            error_list_time.append(np.abs(aggre_time - time_before))
            pbar.set_description("mode:"+my_mode+",avgerror: "+str(float('%.2f' % np.average(error_list)))+", avg_Q5 error: "+str(float('%.2f' % np.average(error_list_time))) +", rate: "+str([float('%.3f' % (x/sum(condition_record))) for x in condition_record]))

    error_file = open("result/error_list_"+my_mode+".txt","w")
    error_file.write(str(error_list))
    SSE = str(float('%.2f' %sum([np.square(x) for x in error_list])))
    MAE = str(float('%.2f' % np.average(error_list)))
    RMSE = str(float('%.2f' %np.sqrt(np.average([np.square(x) for x in error_list]))))
    print(SSE,MAE,RMSE)
    error_file.write("\nSSE: "+str(SSE))
    error_file.write("\nMAE: "+str(MAE))
    error_file.write("\nMAE: "+str(RMSE))

    error_file_time = open("result/error_list_"+my_mode+"_time.txt","w")
    error_file_time.write(str(error_list_time))
    SSE = str(float('%.2f' %sum([np.square(x) for x in error_list_time])))
    MAE = str(float('%.2f' % np.average(error_list_time)))
    RMSE = str(float('%.2f' %np.sqrt(np.average([np.square(x) for x in error_list_time]))))
    print(SSE,MAE,RMSE)
    error_file_time.write("\nSSE: "+str(SSE))
    error_file_time.write("\nMAE: "+str(MAE))
    error_file_time.write("\nMAE: "+str(RMSE))

    # error_file = open("other_data/miss_line_bus.txt","w")
    # error_file.write(str(miss_line))




