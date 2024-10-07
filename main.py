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

print("="*69)
datas = [("台大男一舍前", 61, random.randint(0, 61), random.randint(0, 61)), 
         ("台大新體育館東南側", 39, random.randint(0, 39), random.randint(0, 39)), 
         ("台大總圖書館西南側", 23, random.randint(0, 23), random.randint(0, 23)), 
         ("捷運公館站(2號出口)", 77, random.randint(0, 77), random.randint(0, 77))]

stations = []
for i in datas:
   stations.append(Station(i[0], i[1], i[2], i[3]))

# wage = 200  # 司機的時薪
# drive_times = 4 # 一個小時能載的次數
# oil_price = 3.3 # 油價
# distance = 1    # 行駛的距離
# drive_hourly_cost = wage + oil_price * distance * drive_times   # 請司機的支出
# personal_cost = 3   # 請一個自願者的支出
# bike_per_times = 25 # 每次能運送的YouBike

# 重新分配車輛的函數
def redistribute_bikes(stations):
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


# 先看最一開始的狀況
for station in stations:
    print(station)

redistribute_bikes(stations)

# 印出最終結果(因為類別中有__str__，所以print這個物件會輸出他的訊息)
print("="*69)
for station in stations:
    print(station)