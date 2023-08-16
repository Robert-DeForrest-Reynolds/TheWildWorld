from asyncio import create_task
from time import time

class PlayerObject:
    def __init__(self, Member):
        self.MemberObject = Member
        self.Password = None,
        self.SpecialEnclosure = {}
        self.Inventory = {}
        self.Jobs = {}
        self.PanelOn = False
        self.ProfileCreationDate = int(time())

        self.Profile = {
            "Username": Member.name,
            "Nickname": None,
            "UUID": Member.id,
            "Health": 20,
            "Hunger": 0,
            "Thirst": 0,
            "Sanity": 100,
            "Morale": 500,
            "Age": 1,
        }

        self.Baits = {
            "Common Bait": 0,
            "Rare Bait": 0,
            "Elite Bait": 0,
            "Legendary Bait": 0,
            "Fabled Bait": 0,
            "Divine Bait": 0,
        }

        self.Enclosures = {
            "Nets": 0,
<<<<<<< Updated upstream
            "Aquatic Nets": 0,
=======
>>>>>>> Stashed changes
            "Small Cages": 0,
            "Large Cages": 0,
            "Enormous Cages": 0,
        }
        
        self.Traps = {}

        if self.MemberObject.global_name != None:
            self.Profile["Nickname"] = self.MemberObject.global_name
        else:
            self.Profile["Nickname"] = self.MemberObject.name