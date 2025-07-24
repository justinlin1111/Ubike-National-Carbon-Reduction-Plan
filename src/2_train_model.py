# --- 1. 載入必要套件 ---
import pandas as pd
import numpy as np
from src.train.train_model import train_model

# --- 2. 讀取資料 ---
# 注意：weekday那列是第二列，所以跳過
csv_path = r'data/merged_raw_format_gongguan.csv'  
df = pd.read_csv(csv_path, skiprows=[1])
df.columns = pd.read_csv(csv_path, nrows=0).columns  # 設定正確欄位名稱
print("讀取", csv_path)

# --- 3. 整理資料（展開成直式） ---
df_long = df.melt(id_vars=['station names'], var_name='timestamp', value_name='net_inflow')
print("整理資料")

# --- 4. 擷取時間特徵 ---
df_long['timestamp'] = pd.to_datetime(df_long['timestamp'])
df_long['month'] = df_long['timestamp'].dt.month.astype(np.uint8)
df_long['day'] = df_long['timestamp'].dt.day.astype(np.uint8)
df_long['hour'] = df_long['timestamp'].dt.hour.astype(np.uint8)
df_long['weekday'] = (df_long['timestamp'].dt.weekday + 1).astype(np.uint8)  # 1=Monday, ..., 7=Sunday
df_long['is_holiday'] = df_long['weekday'].isin([6,7]).astype(np.uint8)  # 6=Saturday,7=Sunday是假日

# --- 5. 補缺失值：補中位數 ---
median_value = df_long['net_inflow'].median()
df_long['net_inflow'] = df_long['net_inflow'].fillna(median_value)

train_model('gru', df_long=df_long)
# 要把第一個參數放到config裡面調整比較好