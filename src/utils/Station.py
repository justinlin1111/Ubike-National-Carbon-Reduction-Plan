class Station:
    def __init__(self, name, total, current_bikes, required_bikes) -> None:
        self.name = name                                        # name -> 站點名稱
        self.total = total                                      # total -> 總車柱數
        self.current_bikes = current_bikes                      # current_bikes -> 現有車輛
        self.required_bikes = required_bikes                    # required_bikes -> 需求車輛
        self.diff = self.current_bikes - self.required_bikes    # diff -> current_bikes跟required_bikes的差值

    def __str__(self):
        return f"Station {self.name}: Current Bikes: {self.current_bikes}, Required Bikes: {self.required_bikes}, Diff: {self.diff}"
