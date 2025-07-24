from config import ModelConfig
from src.train.train_xgb import train_xgb_model
from src.train.train_dnn import train_dnn_model
from src.train.train_gru import train_gru_model

def train_model(model_type: str, df_long):
    print("模型為", model_type)
    if model_type == 'xgboost':
        train_xgb_model(df_long, ModelConfig.XGBOOST_PARAMS)
    elif model_type == 'dnn':
        train_dnn_model(df_long, ModelConfig.DNN_PARAMS)
    elif model_type == 'gru':
        train_gru_model(df_long, ModelConfig.GRU_PARAMS)
    else:
        raise ValueError(f"未知的模型類型：{model_type}")
