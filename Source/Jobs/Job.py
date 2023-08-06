from time import time_ns

class Job:
    def __init__(self):
        self.last_harvest = 0

    async def Harvest(self, Player):
        harvest_time = time_ns()
        if harvest_time - self.last_harvest <= 5:
            return f"Cooldown of {harvest_time - self.last_harvest} needed."
        Player.Inventory["Apples"] += self.Output * ( - self.last_harvest)
        self.last_harvest = harvest_time