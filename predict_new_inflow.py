def predict_new_inflow(station_name, timestamp_str):
    import joblib
    import pandas as pd
    import Station
    from getter import getter

    # 載入模型與編碼器
    model = joblib.load(r'lamodel_information/xgb_model.pkl')
    le = joblib.load(r'lamodel_information/label_encoder.pkl')

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
    station = getter(station_name, int(y_pred[0]))
    return station

# import pandas as pd
# df = pd.read_csv(r"youbike_dataset/merged_raw_format_gongguan.csv")
# station_names = df[df['station names'] != 'weekday']['station names'].dropna().tolist()
# # print(station_names)

# year = 2025
# month = 5
# date = 10
# hour = 10
# timestamp = f'{year}-{str(month).zfill(2)}-{str(date).zfill(2)} {str(hour).zfill(2)}:00'

# # print(timestamp)
# for station in station_names:
#     predict_new_inflow(station, timestamp)