import os
import joblib
from math import sqrt
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error

def train_dnn_model(df_long, params):
    le = LabelEncoder()
    df_long['station_id'] = le.fit_transform(df_long['station names'])

    X = df_long[['month', 'day', 'hour', 'weekday', 'is_holiday', 'station_id']]
    y = df_long['net_inflow'].astype(np.float32)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # ✅ 使用 config 中的 hidden_units 建構模型
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=(X_train.shape[1],)))
    for units in params['hidden_units']:
        model.add(tf.keras.layers.Dense(units, activation='relu'))
    model.add(tf.keras.layers.Dense(1))

    model.compile(optimizer='adam', loss='mse')

    print("---fitting---")
    model.fit(
        X_train, y_train,
        validation_split=0.1,
        epochs=params['epochs'],               # ✅ 從 config 讀取
        batch_size=params['batch_size'],       # ✅ 從 config 讀取
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                patience=params['patience'],   # ✅ 從 config 讀取
                restore_best_weights=True
            )
        ]
    )

    y_pred = model.predict(X_test).squeeze()
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    print(f"DNN Test RMSE: {rmse:.2f}")

    outdir = r'model/lamodel_information_dnn'
    os.makedirs(outdir, exist_ok=True)
    model.save(os.path.join(outdir, 'dnn_model.keras'))
    joblib.dump(le, os.path.join(outdir, 'label_encoder.pkl'))
    joblib.dump(scaler, os.path.join(outdir, 'feature_scaler.pkl'))
