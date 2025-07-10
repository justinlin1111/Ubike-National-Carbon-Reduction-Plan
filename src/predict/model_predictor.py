from src.predict.predict_dnn import predict_dnn
from src.predict.predict_xgboost import predict_xgboost

def predict_model(model_type: str, timestamp_str: str, station_str) -> list:
    # 基礎的資訊
    import pandas as pd
    df = pd.read_csv(r"data/merged_raw_format_gongguan.csv")
    station_names = df[df['station names'] != 'weekday']['station names'].dropna().tolist()
    #------------------------------------------------------------
    
    #---確認模型種類與製作Station class---
    if model_type == 'dnn':
        Stations = []
        for station in station_names:
            Stations.append(predict_dnn(timestamp_str, station))
    elif model_type == 'xgboost':
        Stations = []
        for station in station_names:
            Stations.append(predict_xgboost(timestamp_str, station))
    else:
        raise ValueError(f"❌ 不支援的模型類型：{model_type}")
    
    return Stations