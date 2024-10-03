import random

class Station:
    def __init__(self, name, total) -> None:
        self.name = name
        self.total = total
        self.cur = random.randint(0, self.total)
        self.needed = random.randint(0, self.total)
        self.diff = self.cur - self.needed
        self.visited = False


datas = [("台大男一舍前", 61), ("台大新體育館東南側", 39), ("台大總圖書館西南側", 23), ("捷運公館站(2號出口)", 77)]

Stations = []
for i in datas:
   Stations.append(Station(i[0], i[1]))

#chard

wage = 200  # 司機的時薪
drive_times = 4 # 一個小時能載的次數
oil_price = 3.3 # 油價
distance = 1    # 行駛的距離
drive_hourly_cost = wage + oil_price * distance * drive_times   # 請司機的支出
personal_cost = 3   # 請一個自願者的支出
bike_per_times = 25 # 每次能運送的YouBike

# 無D12
for station in Stations:
    # 演算法
    
    pass
