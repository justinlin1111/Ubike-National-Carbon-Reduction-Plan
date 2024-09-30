import random

class Station:
    def __init__(self, name, total) -> None:
        self.name = name
        self.total = total
        self.cur = random.randint(0, self.total)
        self.needed = random.randint(0, self.total)
        self.diff = self.cur - self.needed


datas = [("台大男一舍前", 61), ("台大新體育館東南側", 39), ("台大總圖書館西南側", 23), ("捷運公館站(2號出口)", 77)]

Stations = []
for i in datas:
   Stations.append(Station(i[0], i[1]))



wage = 200
drive_times = 4
oil_price = 3.3
distance = 1
drive_hourly_cost = wage + oil_price * distance * drive_times
personal_cost = 3
bike_per_times = 25

# 無D12
for station in Stations:
    # 演算法
    pass
