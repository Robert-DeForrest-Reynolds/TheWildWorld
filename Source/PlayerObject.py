from asyncio import create_task
from time import time

class PlayerObject:
    def __init__(self, Member):
        self.MemberObject = Member
        self.Password = None,
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

        self.Jobs = {}

        self.Baits = {
            "Common Bait": 0,
            "Rare Bait": 0,
            "Elite Bait": 0,
            "Legendary Bait": 0,
            "Fabled Bait": 0,
            "Divine Bait": 0,
        }

        self.Enlosures = {
            "Common Enclosure": 0,
            "Rare Enclosure": 0,
            "Elite Enclosure": 0,
            "Legendary Enclosure": 0,
            "Fabled Enclosure": 0,
            "Divine Enclosure": 0,
        }
        
        self.Traps = {
            "Common Trap": 0,
            "Rare Trap": 0,
            "Elite Trap": 0,
            "Legendary Trap": 0,
            "Fabled Trap": 0,
            "Divine Trap": 0,
        }

        self.SpecialEnclosure = {}

        self.Inventory = {}
        
        self.PanelOn = False

        if self.MemberObject.global_name != None:
            self.Profile["Nickname"] = self.MemberObject.global_name
        else:
            self.Profile["Nickname"] = self.MemberObject.name