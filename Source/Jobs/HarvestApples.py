from Jobs.Job import Job

class HarvestApples(Job):
    def __init__(self):
        super().__init__()
        self.Name = "Harvest Apples"
        self.OutputItem = "Apple"
        self.Description = "Harvest apples, and sell or cook them."
        self.Level = 1
        self.Output = 0.16 * self.Level
        self.last_harvest = 0
        self.Description