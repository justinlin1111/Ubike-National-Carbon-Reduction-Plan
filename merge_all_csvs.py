import os
import pandas as pd

def merge_original_format(folder_path, output_path):
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

        if merged_df is None:
            merged_df = df
        else:
            # 對齊所有欄位（時間點）
            merged_df = pd.concat([merged_df, df], axis=0)

    # 去除重複站點時間組合（若有）
    merged_df = merged_df.groupby("station names").first().reset_index()

    # 建立 weekday 列（全為空白或指定邏輯，也可以略過）
    # 這裡會用空值填滿欄位數，第一欄為 'weekday'
    weekday_row = ['weekday'] + ['' for _ in range(merged_df.shape[1] - 1)]

    # 將 weekday_row 插入最上方
    merged_df.columns = merged_df.columns.astype(str)  # 確保都是字串
    merged_df_final = pd.DataFrame([weekday_row], columns=merged_df.columns)
    merged_df_final = pd.concat([merged_df_final, merged_df], ignore_index=True)

    # 儲存
    merged_df_final.to_csv(output_path, index=False)
    print(f"\n✅ 合併完成：{output_path}")

# 使用方式
if __name__ == "__main__":
    folder = r"youbike_dataset\net_flow_data"
    output_file = r"youbike_dataset\merged_raw_format.csv"
    merge_original_format(folder, output_file)
