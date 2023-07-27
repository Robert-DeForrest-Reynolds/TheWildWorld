from time import time_ns

class GrowApples:
    def __init__(self):
        self.Name = "Grow Apples"
        self.Description = "Grow apples, and sell or cook them."
        self.Level = 1
        self.Output = 1
        self.last_harvest = 0

    def Harvest(self, Player):
        harvest_time = time_ns()
        if harvest_time - self.last_harvest <= 5:
            return f"Cooldown of {harvest_time - self.last_harvest} needed."
        Player.Inventory["Apples"] += self.Output * ( - self.last_harvest)
        self.last_harvest = harvest_time