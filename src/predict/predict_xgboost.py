def predict_xgboost(timestamp_str, station_name):
    import joblib
    import pandas as pd
    from src.utils.getter import getter

    # 載入模型與編碼器
    model = joblib.load(r'model/lamodel_information_xgboost/xgb_model.pkl')
    le = joblib.load(r'model/lamodel_information_xgboost/label_encoder.pkl')

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

    # 對應禮拜幾的中文字
    weekday_map = {
        1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "日"
    }
    weekday_cn = weekday_map[df['weekday'].iloc[0]]

    print(f"{timestamp_str}（週{weekday_cn}）{station_name} 預測 net inflow：{int(y_pred[0])}")
    # 建立一個Station_list後直接回傳
    station = getter(station_name, round(y_pred[0]))
    return station