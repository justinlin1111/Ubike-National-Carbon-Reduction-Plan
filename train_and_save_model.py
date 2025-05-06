def train_and_save_model(df_long):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    import joblib
    import xgboost as xgb
    import os

    # 編碼 station_id
    le = LabelEncoder()
    df_long['station_id'] = le.fit_transform(df_long['station names'])

    # 特徵與標籤
    X = df_long[['month', 'day', 'hour', 'weekday', 'is_holiday', 'station_id']]
    y = df_long['net_inflow']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=10,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = sqrt(mse)
    print(f"Test MSE: {mse:.2f}")
    print(f"Test RMSE: {rmse:.2f}")

    output_dir = r'lamodel_information'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 儲存模型與編碼器
    joblib.dump(model, os.path.join(output_dir, 'xgb_model.pkl'))
    joblib.dump(le, os.path.join(output_dir, 'label_encoder.pkl'))

# --- 1. 載入必要套件 ---
import pandas as pd
import numpy as np

# --- 2. 讀取資料 ---
# 注意：weekday那列是第二列，所以跳過
csv_path = r'youbike_dataset/merged_raw_format_gongguan.csv'  
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

train_and_save_model(df_long=df_long)
