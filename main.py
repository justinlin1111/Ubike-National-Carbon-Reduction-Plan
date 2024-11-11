import random
from custom_exceptions import SurplusEmptyError, DeficitEmptyError

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

    try:
        check_states(surp, defi)
    except SurplusEmptyError as e:
        print(f"SurplusEmptyError: {e}")
        return  # 捕捉到錯誤後停止運行
    except DeficitEmptyError as e:
        print(f"DeficitEmptyError: {e}")
        return  # 捕捉到錯誤後停止運行
    
    while len(surp)*len(defi) != 0:
        print("="*34 + "調度一次" + "="*34)
        transfer(surp, defi)

# 在transfer前檢查所有站點
# 確保是可以調度的情況
def check_states(surplus_stations:list, deficit_stations:list):
    # 如果有surplus_stations,deficit_stations是空的情況，拋出exception
    if not surplus_stations:
        raise SurplusEmptyError("沒有多餘的車輛可調度")
    elif not deficit_stations:
        raise DeficitEmptyError("沒有站點缺車")
    else:
        print("檢查結果:有車輛需要調度")

# ex:
# 
def transfer(surp: list, defi: list):
    outputLog = []      # 文字輸出初始化
    surp.sort(key = lambda x: x[1], reverse = True)     # 函數先排序，為了優先在同一站載滿車
    defi.sort(key = lambda x: x[1], reverse = True)     #
    print("="*34 + "以下為初始陣列" + "="*35)
    print('surp:', surp)
    print('defi:', defi)
    temp = 0
    
    # surp[]的element是[class Station, abs(Station.diff)]
    for i in range(len(surp)):
        
        # 檢查缺車的站點總和有沒有達到最大裝載量
        # 有就正常執行，沒有就把最大裝載量改成缺車車輛總和
        if (sum([diff_abs[1] for diff_abs in defi])) < bike_per_times:
            max_bike_per_times = (sum([diff_abs[1] for diff_abs in defi]))
        else:
            max_bike_per_times = bike_per_times
        
        # 檢查一個站的車能不能達到最大裝載量
        # 能就直接接收最大裝載量的車，不能就該站的車全接收再往下一站接收
        if (temp + surp[i][1]) >= max_bike_per_times:
            surp[i][1] -= (max_bike_per_times - temp)
            outputLog.append(f'從{surp[i][0].name}接收{max_bike_per_times - temp}台車')
            temp = max_bike_per_times
            
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
    
    print("="*34 + "以下為一次調度Log" + "="*35)
    print(*outputLog, sep = '\n')
    print("="*34 + "以下為一次調度輸出" + "="*35)
    print('surp:', surp)
    print('defi:', defi)
  
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
datas = [("台大男一舍前", 61, random.randint(0, 61), random.randint(0, 61)), 
         ("台大新體育館東南側", 39, random.randint(0, 39), random.randint(0, 39)), 
         ("台大總圖書館西南側", 23, random.randint(0, 23), random.randint(0, 23)), 
         ("捷運公館站(2號出口)", 77, random.randint(0, 77), random.randint(0, 77))]
stations = []
for i in datas:
   stations.append(Station(i[0], i[1], i[2], i[3]))

wtf = [-10, -10, -10, 10]
for i in range(len(wtf)):
    stations[i].diff = wtf[i]

# 車輛調度
redistribute_bikes(stations)

'''
輸出
調度完的結果
調度花費

to do list:
1.意願函數 假設 100
    車子 100 + 油錢(先不考慮/3.3 * 0.7 ntd/km)
    意願 100% 費用 5
    <=20騎 相反 車載
2.意願不是100討論期望值
    def 意願函數(費用 距離)
4.



'''