import json
import ssl
import urllib.request
from Station import Station

# 做成一個函式
# 要先知道需要哪些因子，可以弄成一個pandas(?
def getter(station_name, require_bike) -> Station:
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    context = ssl._create_unverified_context()

    with urllib.request.urlopen(url, context=context) as jsondata:
        # 將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
        datas = json.loads(jsondata.read().decode('utf-8-sig')) 

    # 格式化每一行的內容
    for data in datas:
        if data['sna'] == ('YouBike2.0_' + station_name):
            print(data['sna'] + 'exist')
            return Station(station_name, data['total'], data['available_rent_bikes'], require_bike)
    #     print(data['sna'])
    #     print("可用車輛數:" + str(data['available_rent_bikes']))
    #     print("車柱總數: " + str(data['total']))
    #     print("站點更新時間: " + data['mday'])
    #     print()
