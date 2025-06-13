import pandas as pd
import numpy as np
import joblib
import tensorflow as tf

# predict from model
def predict_one(timestamp_str, station, model_dir='lamodel_information_dnn'):
    ts = pd.Timestamp(timestamp_str, tz='Asia/Taipei')

    feats = {
        'month'     : ts.month,
        'day'       : ts.day,
        'hour'      : ts.hour,
        'weekday'   : ts.dayofweek + 1,
        'is_holiday': 1 if ts.dayofweek + 1 in (6, 7) else 0,
        'station_id': joblib.load(f'{model_dir}/label_encoder.pkl').transform([station])[0]
    }
    X = pd.DataFrame([feats])

    scaler = joblib.load(f'{model_dir}/feature_scaler.pkl')
    X_scaled = scaler.transform(X)

    model = tf.keras.models.load_model(f'{model_dir}/dnn_model.keras')
    pred = model.predict(X_scaled, verbose=0)[0, 0]
    return float(pred)

# compare
def do_predict(ts_str, station):
    pred = predict_one(ts_str, station)
    print(f"[預測] {ts_str} {station} => {pred}")
    
    # for comparison

    csv_path = r'youbike_dataset/merged_raw_format_gongguan.csv'
    df = pd.read_csv(csv_path, skiprows=[1])
    df.columns = pd.read_csv(csv_path, nrows=0).columns
    df_long = df.melt(id_vars=['station names'],
                    var_name='timestamp',
                    value_name='net_inflow')
    df_long['timestamp'] = pd.to_datetime(df_long['timestamp'])

    """
        ts_str  : 'YYYY-MM-DD HH:MM'(例如 '2024-06-15 18:00')
        station : '捷運公館站(1號出口)' 之類
        df_long : 長格式 DataFrame
    """
    
    ts = pd.Timestamp(ts_str, tz='Asia/Taipei')
    
    cond = (
        (df_long['station names'] == station) &
        (df_long['timestamp'].dt.month == ts.month) &
        (df_long['timestamp'].dt.day   == ts.day) &
        (df_long['timestamp'].dt.hour  == ts.hour)
    )
    
    actual_rows = df_long.loc[cond, ['station names', 'timestamp', 'net_inflow']]
    
    if actual_rows.empty:
        print("[DATA] 找不到任何同月/日/時的實際紀錄")
    else:
        for _, row in actual_rows.sort_values('timestamp').iterrows():
            tstr = row['timestamp'].strftime('%Y-%m-%d %H:%M')
            print(f"[資料集] {tstr} {row['station names']} => {row['net_inflow']}")

# main
do_predict('2024-06-15 18:00', '捷運公館站(1號出口)')