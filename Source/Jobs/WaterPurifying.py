from Jobs.Job import Job

class WaterPurifying(Job):
    def __init__(self):
        super().__init__()
        self.Name = "Water Purifying"
        self.OutputItem = "Clean Water"
        self.Description = "Purify water that the Hold supplies. You do not get clean water from this job."
        self.Level = 1
        self.Output = 0.16 * self.Level
        self.LastHarvest = 0