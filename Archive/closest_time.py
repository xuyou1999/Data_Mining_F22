import pandas as pd
import time
calender_df = pd.read_csv("other_data/stop_times_midnuit_fid_15days_time_before_after_2_less_than_6.csv").sort_values(by='arrival_time')
calender_df["arrival_time"] = pd.to_datetime(calender_df["arrival_time"])
print(calender_df.dtypes)
d_v1_distinct_time_df = pd.read_csv("other_data/d_v1_distinct_time_fid.csv").sort_values(by='time')
d_v1_distinct_time_df.rename(columns={'time':'time_before'}, inplace= True)
print(d_v1_distinct_time_df.dtypes)
d_v1_distinct_time_df["time_before"] = pd.to_datetime(d_v1_distinct_time_df["time_before"])

merge_table = pd.merge_asof(calender_df, d_v1_distinct_time_df, left_on="arrival_time", right_on="time_before", left_by="fid_lines", right_by="fid_lines",
                            direction="backward")

d_v1_distinct_time_df2 = pd.read_csv("other_data/d_v1_distinct_time_fid.csv").sort_values(by='time')
d_v1_distinct_time_df2.rename(columns={'time':'time_after'}, inplace= True)
print(d_v1_distinct_time_df2.dtypes)
d_v1_distinct_time_df2["time_after"] = pd.to_datetime(d_v1_distinct_time_df2["time_after"])

merge_table = pd.merge_asof(merge_table, d_v1_distinct_time_df2, left_on="arrival_time", right_on="time_after", left_by="fid_lines", right_by="fid_lines",
                            direction="forward")


print(merge_table)
merge_table.to_csv("other_data/merge_arrive_time.csv")