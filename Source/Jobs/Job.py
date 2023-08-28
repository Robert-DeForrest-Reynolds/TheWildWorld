from uuid import uuid4
from time import time

class Job:
    def __init__(self):
        self.LastHarvest = 0
        self.OutputItem = None
        self.OwnerUUID = None
        self.UUID = uuid4().hex

        # Termination Date is set 3 real life days from time job is created and given to player 259200
        self.TerminationDate = int(time()) + 20

    async def Harvest(self, Player):
        HarvestTime = time()
        print(HarvestTime)
        print(self.LastHarvest)
        if self.LastHarvest == 0:
            HarvestAmount = round(self.Output * (HarvestTime - Player.ProfileCreationDate), 2)
        else:
            HarvestAmount = round(self.Output * (HarvestTime - self.LastHarvest), 2)

        if self.OutputItem not in Player.Inventory.keys():
            Player.Inventory.update({self.OutputItem:HarvestAmount})
        else:
            Player.Inventory[self.OutputItem] += HarvestAmount
        self.LastHarvest = HarvestTime
        return("Success", HarvestAmount)
