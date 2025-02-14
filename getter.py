import json
import ssl
import urllib.request

# 做成一個函式
# 要先知道需要哪些因子，可以弄成一個pandas(?
url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
context = ssl._create_unverified_context()

with urllib.request.urlopen(url, context=context) as jsondata:
    # 將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
    datas = json.loads(jsondata.read().decode('utf-8-sig')) 

# 格式化每一行的內容
for data in datas:
    print(data['sna'])
    print("可用車輛數:" + str(data['available_rent_bikes']))
    print("車輛總數: " + str(data['total']))
    print("站點更新時間: " + data['mday'])
    print()

# 已經有人在github上面實作出歷史數據(十分鐘抓一次，抓一天的)
# https://github.com/tses89214/youbike-historical-data/tree/main/data