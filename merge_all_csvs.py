import os
import pandas as pd
from categories import gongguan_stations

def merge_original_format(folder_path, output_path, specified_stations):
    merged_df = None

    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".csv"):
            continue

        file_path = os.path.join(folder_path, filename)
        print(f"處理檔案: {filename}")

        # 讀取第一列（標題）與資料（略過第二列的 weekday）
        df = pd.read_csv(file_path, skiprows=[1])

        # 確保欄位名稱正確
        df.columns = pd.read_csv(file_path, nrows=0).columns

        # ✅ 只保留公館站點的資料
        df = df[df['station names'].isin(specified_stations)]

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.concat([merged_df, df], axis=0)

    # 去除重複站點時間組合（依照站名唯一保留第一筆）
    merged_df = merged_df.groupby("station names").first().reset_index()

    # ➕ 強制轉換數值欄位為 Int64（可含空值的整數）
    for col in merged_df.columns:
        if col != "station names":
            merged_df[col] = pd.to_numeric(merged_df[col], errors="coerce").astype("Int64")

    # 建立 weekday 列（第一欄為 weekday，其他為空值）
    weekday_row = ['weekday'] + ['' for _ in range(merged_df.shape[1] - 1)]

    # 插入 weekday_row 作為第一列
    merged_df.columns = merged_df.columns.astype(str)
    merged_df_final = pd.DataFrame([weekday_row], columns=merged_df.columns)
    merged_df_final = pd.concat([merged_df_final, merged_df], ignore_index=True)

    # 儲存結果
    merged_df_final.to_csv(output_path, index=False)
    print(f"\n✅ 合併完成（僅限公館站點）：{output_path}")

# 使用方式
if __name__ == "__main__":
    folder = r"youbike_dataset/net_flow_data"
    output_file = r"youbike_dataset/merged_raw_format_gongguan.csv"
    merge_original_format(folder, output_file, gongguan_stations)
