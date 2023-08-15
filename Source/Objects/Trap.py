class Trap:
    def __init__(self, Name):
        self.Name = Name
        self.Bait = Name.split(" - ")[0]
        self.Enclosure = Name.split(" - ")[1]