from time import time_ns
from Jobs.Job import Job

class ChopTrees(Job):
    def __init__(self):
        self.Name = "Chop Trees"
        self.Description = "Chop trees down harvesting lumbar for a multitude of uses."
        self.Level = 1
        self.Output = 1
        self.last_harvest = 0
        super.__init__()