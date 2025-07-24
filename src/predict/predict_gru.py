import pandas as pd
import numpy as np
import os
from config import PathConfig
import joblib
import tensorflow as tf

# predict from GRU model
def predict_one(timestamp_str, station):
    model_dir = os.path.join(PathConfig.MODEL_DIR, 'lamodel_information_gru')

    # 準備靜態特徵
    ts = pd.Timestamp(timestamp_str, tz='Asia/Taipei')
    feats = {
        'month': ts.month,
        'day': ts.day,
        'hour': ts.hour,
        'weekday': ts.dayofweek + 1,
        'is_holiday': 1 if ts.dayofweek + 1 in (6, 7) else 0
    }

    # 編碼站點
    label_encoder = joblib.load(os.path.join(model_dir, 'label_encoder.pkl'))
    feats['station_id'] = label_encoder.transform([station])[0]

    # 放入 DataFrame
    X = pd.DataFrame([feats])

    # 特徵縮放
    scaler = joblib.load(os.path.join(model_dir, 'feature_scaler.pkl'))
    X_scaled = scaler.transform(X)

    # ✅ 包成 (1, 1, num_features) 給 GRU
    X_scaled_seq = X_scaled.reshape((1, 1, X_scaled.shape[1]))

    # 載入 GRU 模型
    model = tf.keras.models.load_model(os.path.join(model_dir, 'gru_model.keras'))
    pred = model.predict(X_scaled_seq, verbose=0)[0, 0] # type: ignore
    return float(pred)

# compare
def predict_gru(ts_str, station):
    from src.utils.getter import getter
    pred = predict_one(ts_str, station)
    print(f"[預測] {ts_str} {station} => {pred}")
    
    station = getter(station, round(pred))
    return station
