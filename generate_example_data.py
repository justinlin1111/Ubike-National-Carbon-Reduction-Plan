import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 參數設定 ---
num_stations = 5
station_names = [f"Station {chr(65+i)}" for i in range(num_stations)]
start_time = datetime(2023, 1, 1, 0)
end_time = datetime(2024, 1, 1, 0)  # 到 2023-12-31 23:00 為止
timestamps = pd.date_range(start=start_time, end=end_time, freq='h')[:-1]
timestamp_strs = [ts.isoformat() + "+08:00" for ts in timestamps]
weekday_strs = [ts.strftime('%A') for ts in timestamps]

# --- 模擬流量資料 ---
def generate_inflow_data(ts):
    hour = ts.hour
    day_of_week = ts.weekday()  # 0=Mon ... 6=Sun
    
    # 模擬：平日早晚高峰高流量，假日中午略高
    if day_of_week < 5:  # 平日
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            return np.random.randint(8, 15)
        else:
            return np.random.randint(-2, 6)
    else:  # 假日
        if 11 <= hour <= 13:
            return np.random.randint(4, 10)
        else:
            return np.random.randint(-3, 5)

# --- 建立資料 ---
data = []
for station in station_names:
    flow = [generate_inflow_data(ts) for ts in timestamps]
    data.append(flow)

# --- 建立 DataFrame ---
df = pd.DataFrame(data, index=station_names, columns=timestamp_strs)
df.index.name = 'station names'

# 加入 weekday 作為第二列
weekday_row = pd.DataFrame([weekday_strs], index=['weekday'], columns=timestamp_strs)

# 合併 weekday 與主資料
df_final = pd.concat([weekday_row, df])

# 加入欄位名稱補全（確保 index 也有名字）
df_final.index.name = 'station names'

# --- 輸出 CSV，保留 index 並避免 header 遺失 ---
output_path = "generated_youbike_2023.csv"
df_final.to_csv(output_path, index=True)
print(f"✅ 成功產生：{output_path}")
