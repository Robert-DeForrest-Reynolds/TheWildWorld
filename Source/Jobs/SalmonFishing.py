from Jobs.Job import Job

class SalmonFishing(Job):
    def __init__(self):
        super().__init__()
        self.Name = "Salmon Fishing"
        self.OutputItem = "Salmon"
        self.Description = "Fish for salmon in the Caswell River."
        self.Level = 1
        self.Output = 0.16 * self.Level
        self.LastHarvest = 0