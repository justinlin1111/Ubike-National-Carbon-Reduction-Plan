import os
from src.utils.data_transform import data_transform
from src.utils.getter import load_gongguan_stations
from src.utils.merge_all_csvs import merge_all_csvs

# 確保資料夾存在，不存在會直接創建資料夾
os.makedirs(r"data/net_flow_data", exist_ok=True)

for i in range(1, 12+1):
    print("正在轉換資料:", r"data/raw_data_csv/2023" + str(i).zfill(2) + "_轉乘YouBike2.0票證刷卡資料.csv")
    data_transform(
        r"data/raw_data_csv/2023" + str(i).zfill(2) + "_轉乘YouBike2.0票證刷卡資料.csv",
        r"data/net_flow_data/2023" + str(i).zfill(2) + ".csv"
    )

#---合併csv---
folder = r"data/net_flow_data"
output_file = r"data/merged_raw_format_gongguan.csv"
gongguan_list = load_gongguan_stations()
print("---合併所有csv---")
merge_all_csvs(folder, output_file, gongguan_list)
