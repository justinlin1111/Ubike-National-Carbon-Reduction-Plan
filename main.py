from predict_new_inflow import predict_new_inflow
from genetic_algorithm import genetic_algorithm

if __name__ == "__main__":
    print("hello world")
    # 先把Station做出來
    print('make Station')
    import pandas as pd
    df = pd.read_csv(r"youbike_dataset/merged_raw_format_gongguan.csv")
    station_names = df[df['station names'] != 'weekday']['station names'].dropna().tolist()
    # print(station_names)

    # 時間參數
    year = 2025
    month = 5
    date = 10
    hour = 10
    timestamp = f'{year}-{str(month).zfill(2)}-{str(date).zfill(2)} {str(hour).zfill(2)}:00'

    # print(timestamp)
    Stations = []
    for station in station_names:
        Stations.append(predict_new_inflow(station, timestamp))
    # print(Stations)
    # print(Stations[0].name)
    # 看要怎麼把預測出來的結果放到Station裡面
    solutions = genetic_algorithm(Stations)
    for station, allocation in zip(Stations, solutions):
        if allocation < 0:
            print(f"{station.name}需要移走{allocation}輛車")
        elif allocation > 0:
            print(f"{station.name}需要移入{allocation}輛車")
    # 處理多車少車的情況
    # 應該就好了