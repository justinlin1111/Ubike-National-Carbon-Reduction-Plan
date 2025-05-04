def predict_new_inflow(station_name, timestamp_str):
    import joblib
    import pandas as pd

    # 載入模型與編碼器
    model = joblib.load(r'lamodel_information\xgb_model_example.pkl')
    le = joblib.load(r'lamodel_information\label_encoder_example.pkl')

    # 建立 DataFrame
    df = pd.DataFrame({
        'station names': [station_name],
        'timestamp': [timestamp_str]
    })

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['month'] = df['timestamp'].dt.month.astype('uint8')
    df['day'] = df['timestamp'].dt.day.astype('uint8')
    df['hour'] = df['timestamp'].dt.hour.astype('uint8')
    df['weekday'] = (df['timestamp'].dt.weekday + 1).astype('uint8')
    df['is_holiday'] = df['weekday'].isin([6, 7]).astype('uint8')
    df['station_id'] = le.transform(df['station names'])

    X_new = df[['month', 'day', 'hour', 'weekday', 'is_holiday', 'station_id']]
    y_pred = model.predict(X_new)

    print(f"{timestamp_str} {station_name} 預測 net inflow：{y_pred[0]:.2f}")
    return y_pred[0]

predict_new_inflow('Station A', '2025-05-04 11:00')