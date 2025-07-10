import os

class PathConfig:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    NET_FLOW_DIR = os.path.join(DATA_DIR, 'net_flow_data')
    PROCESSED_RENT = os.path.join(DATA_DIR, 'processed_data_rent')
    PROCESSED_RETURN = os.path.join(DATA_DIR, 'processed_data_return')

    # 可以根據需求加上你常用的檔案路徑
    GENERATED_CSV = os.path.join(DATA_DIR, 'generated_youbike_2023.csv')


class ModelConfig:
    MODEL_TYPE = 'dnn'  # or 'xgboost'
    OUTPUT_DIR = PathConfig.MODEL_DIR  # 使用上面的路徑

    XGBOOST_PARAMS = {
        'n_estimators': 200,
        'max_depth': 10,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42
    }

    DNN_PARAMS = {
        'epochs': 100,
        'batch_size': 1024,
        'hidden_units': [256, 256],
        'patience': 8
    }
