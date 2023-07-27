from time import time_ns

class ChopTrees:
    def __init__(self):
        self.Name = "Chop Trees"
        self.Description = "Chop trees down harvesting lumbar for a multitude of uses."
        self.Level = 1
        self.Output = 1
        self.last_harvest = 0

    def Harvest(self, Player):
        harvest_time = time_ns()
        if harvest_time - self.last_harvest <= 5:
            return f"Cooldown of {harvest_time - self.last_harvest} needed."
        Player.Inventory["Lumber"] += self.Output * ( - self.last_harvest)
        self.last_harvest = harvest_time