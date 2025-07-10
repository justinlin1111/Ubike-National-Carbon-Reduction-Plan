def train_xgb_model(df_long, params):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    import joblib
    import xgboost as xgb
    import os
    from config import PathConfig  # 加入 centralized 路徑

    # 編碼 station_id
    le = LabelEncoder()
    df_long['station_id'] = le.fit_transform(df_long['station names'])

    # 特徵與標籤
    X = df_long[['month', 'day', 'hour', 'weekday', 'is_holiday', 'station_id']]
    y = df_long['net_inflow']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ✅ 使用 centralized 的 XGBoost 超參數
    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = sqrt(mse)
    print(f"Test MSE: {mse:.2f}")
    print(f"Test RMSE: {rmse:.2f}")

    # ✅ 使用 centralized 輸出資料夾
    output_dir = os.path.join(PathConfig.MODEL_DIR, 'lamodel_information_xgboost')
    os.makedirs(output_dir, exist_ok=True)

    # 儲存模型與編碼器
    print("---儲存模型與編碼器---")
    joblib.dump(model, os.path.join(output_dir, 'xgb_model.pkl'))
    joblib.dump(le, os.path.join(output_dir, 'label_encoder.pkl'))
