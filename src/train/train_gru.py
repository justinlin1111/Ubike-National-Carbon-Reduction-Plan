def train_gru_model(df_long, params):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    import joblib
    import tensorflow as tf
    from tensorflow.keras import layers, models # type: ignore
    import os
    from config import PathConfig

    # ✅ 編碼站點名稱
    le = LabelEncoder()
    df_long['station_id'] = le.fit_transform(df_long['station names'])

    # ✅ 特徵與標籤
    feature_cols = ['month', 'day', 'hour', 'weekday', 'is_holiday', 'station_id']
    X = df_long[feature_cols]
    y = df_long['net_inflow'].values

    # ✅ 特徵標準化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ✅ Reshape 為 (samples, time_steps=1, features)
    X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

    # ✅ 分割資料集
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # ✅ 建立 GRU 模型
    model = models.Sequential([
        layers.GRU(params.get("units", 32), input_shape=(1, X_scaled.shape[2])),
        layers.Dense(1)
    ])

    model.compile(optimizer=params.get("optimizer", "adam"), loss="mse")

    # ✅ 模型訓練
    model.fit(X_train, y_train, epochs=params.get("epochs", 50), batch_size=params.get("batch_size", 32), verbose=1)

    # ✅ 評估模型
    y_pred = model.predict(X_test, verbose=0)
    mse = mean_squared_error(y_test, y_pred)
    rmse = sqrt(mse)
    print(f"Test MSE: {mse:.2f}")
    print(f"Test RMSE: {rmse:.2f}")

    # ✅ 儲存模型與編碼器
    output_dir = os.path.join(PathConfig.MODEL_DIR, 'lamodel_information_gru')
    os.makedirs(output_dir, exist_ok=True)
    print("---儲存 GRU 模型與編碼器---")

    model.save(os.path.join(output_dir, 'gru_model.keras'))
    joblib.dump(le, os.path.join(output_dir, 'label_encoder.pkl'))
    joblib.dump(scaler, os.path.join(output_dir, 'feature_scaler.pkl'))
