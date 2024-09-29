class Station:
    def __init__(self, name, total) -> None:
        self.name = name
        self.total = total
        

Station1 = Station("台大男一舍前", 61)
Station2 = Station("台大新體育館東南側", 39)
Station3 = Station("台大總圖書館西南側", 23)
Station4 = Station("捷運公館站(2號出口)", 77)

wage = 200
drive_times = 4
oil_price = 3.3
distance = 1
drive_hourly_cost = wage + oil_price * distance * drive_times
personal_cost = 3
