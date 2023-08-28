from Jobs.Job import Job

class ChopOakTrees(Job):
    def __init__(self):
        super().__init__()
        self.Name = "Chop Oak Trees"
        self.OutputItem = "Oak Log"
        self.Description = "Chop oak trees down harvesting lumber for a multitude of uses."
        self.Level = 1
        self.Output = 0.16 * self.Level
        self.LastHarvest = 0