from Jobs.Job import Job

class MineCoal(Job):
    def __init__(self):
        super().__init__()
        self.Name = "Mine Coal"
        self.OutputItem = "Coal"
        self.Description = "Mine coal and sell it, or use it as fuel to power your equipment."
        self.Level = 1
        self.Output = 0.16 * self.Level
        self.LastHarvest = 0
