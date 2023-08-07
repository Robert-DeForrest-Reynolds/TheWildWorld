from Jobs.Job import Job

class ChopTrees(Job):
    def __init__(self):
        super().__init__()
        self.Name = "Chop Trees"
        self.OutputItem = "Logs"
        self.Description = "Chop trees down harvesting lumber for a multitude of uses."
        self.Level = 1
        self.Output = 0.16 * self.Level
        self.last_harvest = 0