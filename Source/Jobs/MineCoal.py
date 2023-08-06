from time import time_ns

class MineCoal:
    def __init__(self):
        self.Name = "Mine Coal"
        self.Description = "Mine coal and sell it, or use it as fuel to power your equipment."
        self.Level = 1
        self.Output = 1
        self.last_harvest = 0
        super.__init__()
