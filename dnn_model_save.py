import pandas as pd
import numpy as np


# 和 xgboost 相同
csv_path = r'youbike_dataset/merged_raw_format_gongguan.csv'
df = pd.read_csv(csv_path, skiprows=[1])                 # 去掉 weekday 那列
df.columns = pd.read_csv(csv_path, nrows=0).columns

df_long = df.melt(id_vars=['station names'],
                  var_name='timestamp',
                  value_name='net_inflow')

df_long['timestamp'] = pd.to_datetime(df_long['timestamp'])
df_long['month']   = df_long['timestamp'].dt.month.astype(np.uint8)
df_long['day']     = df_long['timestamp'].dt.day.astype(np.uint8)
df_long['hour']    = df_long['timestamp'].dt.hour.astype(np.uint8)
df_long['weekday'] = (df_long['timestamp'].dt.weekday + 1).astype(np.uint8)
df_long['is_holiday'] = df_long['weekday'].isin([6, 7]).astype(np.uint8)

df_long['net_inflow'] = df_long['net_inflow'].fillna(df_long['net_inflow'].median())


def train_and_save_dnn(df_long):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    import tensorflow as tf
    import joblib, os

    le = LabelEncoder()
    df_long['station_id'] = le.fit_transform(df_long['station names'])

    X = df_long[['month', 'day', 'hour', 'weekday', 'is_holiday', 'station_id']]
    y = df_long['net_inflow'].astype(np.float32)

    # --------- 標準化（有助於 DNN 收斂）---------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(1)                  # 輸出單一數值
    ])
    model.compile(optimizer='adam', loss='mse')
    model.summary()

    model.fit(
        X_train, y_train,
        validation_split=0.1,
        epochs=100,
        batch_size=1024,
        callbacks=[tf.keras.callbacks.EarlyStopping(patience=8,
                                                    restore_best_weights=True)]
    )

    y_pred = model.predict(X_test).squeeze()
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    print(f'DNN Test RMSE = {rmse:.2f}')

    outdir = 'lamodel_information_dnn'
    os.makedirs(outdir, exist_ok=True)
    model.save(os.path.join(outdir, 'dnn_model.keras'))
    joblib.dump(le,      os.path.join(outdir, 'label_encoder.pkl'))
    joblib.dump(scaler,  os.path.join(outdir, 'feature_scaler.pkl'))
    
train_and_save_dnn(df_long)
