import random

class Station:
    # name -> 站點名稱
    # total -> 總車柱數
    # current_bikes -> 現有車輛
    # required_bikes -> 需求車輛
    # diff -> current_bikes跟required_bikes的差值
    def __init__(self, name, total, current_bikes, required_bikes) -> None:
        self.name = name
        self.total = total
        self.current_bikes = current_bikes
        self.required_bikes = required_bikes
        self.diff = self.current_bikes - self.required_bikes

    def __str__(self):
        return f"Station {self.name}: Current Bikes: {self.current_bikes}, Required Bikes: {self.required_bikes}, Diff: {self.diff}"

def redistribute_bikes(stations):
    
    surp = [[surp_stations, abs(surp_stations.diff)] for surp_stations in stations if surp_stations.diff > 0]
    defi = [[defi_stations, abs(defi_stations.diff)] for defi_stations in stations if defi_stations.diff < 0]

    while len(surp)*len(defi) != 0:
        transfer(surp, defi)
    
    print(surp)
    print(defi)
    
    '''
    # 選出 diff > 0 跟 diff < 0 的
    surplus_stations = [station for station in stations if station.diff > 0]
    deficit_stations = [station for station in stations if station.diff < 0]

    # 如果還有多出來可以調度的車的話(即diff > 0)
    for surplus_station in surplus_stations:
        for deficit_station in deficit_stations:
            if surplus_station.diff == 0:
                break
            if deficit_station.diff == 0:
                continue

            # 因為只需要移動多出來的可調度車輛，但同時可能需要的不一定那麼多，選小的
            transfer_amount = min(surplus_station.diff, -deficit_station.diff)
        
            # 把調度後的結果寫出來
            surplus_station.current_bikes -= transfer_amount
            surplus_station.diff -= transfer_amount

            deficit_station.current_bikes += transfer_amount
            deficit_station.diff += transfer_amount
            print(f"從{surplus_station.name}調了{transfer_amount}台車到{deficit_station.name}")
    '''
            
def transfer(surp: list, defi: list):
    outputLog = []      # 文字輸出初始化
    surp.sort(key = lambda x: x[1], reverse = True)     # 函數先排序，為了優先在同一站載滿車
    defi.sort(key = lambda x: x[1], reverse = True)     #
    print('surp:', surp)
    print('defi:', defi)
    print("="*34 + "以上為初始陣列" + "="*35)
    temp = 0
    
    # surp[]的element是[class Station, abs(Station.diff)]
    for i in range(len(surp)):
        
        # 檢查缺車的站點總合有沒有達到最大裝載量
        # 有就正常執行，沒有就把最大裝載量改成缺車車輛總和
        if (sum([diff_abs[1] for diff_abs in defi])) < bike_per_times:
            max_bike_per_times = (sum([diff_abs[1] for diff_abs in defi]))
        else:
            max_bike_per_times = bike_per_times
        
        # 檢查一個站的車能不能達到最大裝載量
        # 能就直接接收最大裝載量的車，不能就該站的車全接收再往下一站接收
        if (temp + surp[i][1]) >= max_bike_per_times:
            surp[i][1] -= (max_bike_per_times - temp)
            temp = max_bike_per_times
            outputLog.append(f'從{surp[i][0].name}接收{temp}台車')
            break
        else:
            temp += surp[i][1]
            outputLog.append(f'從{surp[i][0].name}接收{surp[i][1]}台車')
            surp[i][1] = 0


    # defi[]的element是[class Station, abs(Station.diff)]
    for i in range(len(defi)):
        
        # 檢查缺車的站點是否小於接收到的總車輛
        # 是就把該站送送滿再送剩下的車，不是就把車全送過去 
        if (defi[i][1] < temp):
            temp -= defi[i][1]
            outputLog.append(f'將{defi[i][1]}台車送達{defi[i][0].name}')
            defi[i][1] = 0
        else:
            defi[i][1] -= temp
            outputLog.append(f'將{temp}台車送達{defi[i][0].name}')
            break
    
    # 把供需滿足的車站從陣列刪除 pass by shared
    lst_temp = surp.copy()
    surp.clear()
    surp.extend([i for i in lst_temp if i[1] != 0])
    surp = [i for i in lst_temp if i[1] != 0]
    lst_temp = defi.copy()
    defi.clear()
    defi.extend([i for i in lst_temp if i[1] != 0])
    
    print('surp:', surp)
    print('defi:', defi)
    print("="*34 + "以上為一次調度輸出" + "="*35)
    print(*outputLog, sep = '\n')
    print("="*34 + "以上為一次調度Log" + "="*35)
    
  
# =================================參數====================================
# wage = 200  # 司機的時薪
# drive_times = 4 # 一個小時能載的次數
# oil_price = 3.3 # 油價
# distance = 1    # 行駛的距離
# drive_hourly_cost = wage + oil_price * distance * drive_times   # 請司機的支出
# personal_cost = 3   # 請一個自願者的支出
bike_per_times = 25 # 每次能運送的YouBike
# ========================================================================


# 前置作業
# 讀入站點資訊
print("="*69)
datas = [("台大男一舍前", 61, random.randint(0, 61), random.randint(0, 61)), 
         ("台大新體育館東南側", 39, random.randint(0, 39), random.randint(0, 39)), 
         ("台大總圖書館西南側", 23, random.randint(0, 23), random.randint(0, 23)), 
         ("捷運公館站(2號出口)", 77, random.randint(0, 77), random.randint(0, 77))]
stations = []
for i in datas:
   stations.append(Station(i[0], i[1], i[2], i[3]))

# 車輛調度
redistribute_bikes(stations)

'''
輸出
調度完的結果
調度花費

系統
加入人體調度
意願 100% 費用 5
def 意願函數(費用 距離)



'''