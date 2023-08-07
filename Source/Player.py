from asyncio import create_task
from time import time

class Player:
    def __init__(self, Member):
        self.Profile = {
            "Member Object": Member,
            "Username": Member.name,
            "Nickname": None,
            "UUID": Member.id,
            "Password": None,
            "Health": 20,
            "Hunger": 0,
            "Thirst": 0,
            "Sanity": 100,
            "Morale": 500,
            "Age": 1,
            "Jobs": {},
            "Profile Created Date": int(time()),
        }

        self.Inventory = {}
        
        self.PanelOn = False

        if self.Profile["Member Object"].global_name != None:
            self.Profile["Nickname"] = self.Profile["Member Object"].global_name
        else:
            self.Profile["Nickname"] = self.Profile["Member Object"].name