from time import time_ns

class MineCoal:
    def __init__(self):
        self.Name = "Mine Coal"
        self.Description = "Mine coal and sell it, or use it as fuel to power your equipment."
        self.Level = 1
        self.Output = 1
        self.last_harvest = 0

    def Harvest(self, Player):
        harvest_time = time_ns()
        if harvest_time - self.last_harvest <= 5:
            return f"Cooldown of {harvest_time - self.last_harvest} needed."
        Player.Inventory["Coal"] += self.Output * ( - self.last_harvest)
        self.last_harvest = harvest_time