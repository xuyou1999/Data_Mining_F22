import pandas as pd
df = pd.read_csv("other_data/data1206.csv")
print(df.dtypes)
df = df.loc[:,["time","mode","vehicle_x","vehicle_y", "directionid", "lineid", "speed_meter_second"]]
df = df[df["lineid"]==95]
df["vehicle_x"] = df["vehicle_x"].astype(int)
df["vehicle_y"] = df["vehicle_y"].astype(int)
df["speed_meter_second"] = df["speed_meter_second"].map('{:,.4f}'.format)
df.to_csv("other_data/simplified_data.csv",index=False)