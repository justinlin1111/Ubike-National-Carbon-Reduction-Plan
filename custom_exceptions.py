class EmptyError(Exception):
    pass

class SurplusEmptyError(EmptyError):
    def __init__(self, message="沒有多餘的車輛可調度"):
        self.message = message
        super().__init__(self.message)

class DeficitEmptyError(EmptyError):
    def __init__(self, message="沒有站點缺車"):
        self.message = message
        super().__init__(self.message)

    