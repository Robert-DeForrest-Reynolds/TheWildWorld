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

        self.Inventory = {}
        
        self.PanelOn = False

        if self.MemberObject.global_name != None:
            self.Profile["Nickname"] = self.MemberObject.global_name
        else:
            self.Profile["Nickname"] = self.MemberObject.name