from Jobs.Job import Job

class HarvestWheat(Job):
    def __init__(self):
        super().__init__()
        self.Name = "Harvest Wheat"
        self.OutputItem = "Wheat"
        self.Description = "Harvest Wheat, and sell them or cook them."
        self.Level = 1
        self.Output = 0.16 * self.Level
        self.LastHarvest = 0