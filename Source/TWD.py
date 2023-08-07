from sqlite3 import connect
from asyncio import create_task
from Player import Player
from Jobs.HarvestApples import HarvestApples
from Jobs.ChopTrees import ChopTrees
from Jobs.MineCoal import MineCoal

PLAYER_TABLE = """\
UUID INTEGER DEFAULT 0 PRIMARY KEY,\
Username TEXT DEFAULT NONE,\
Nickname TEXT DEFAULT NONE,\
Password TEXT DEFAULT NONE,\
Experience INTEGER DEFAULT 0,\
Level INTEGER DEFAULT 1,\
Wallet INTEGER DEFAULT 0,\
Health INTEGER DEFAULT 5000,\
Hunger INTEGER DEFAULT 0,\
Thirst INTEGER DEFAULT 0,\
Sanity INTEGER DEFAULT 0,\
Morale INTEGER DEFAULT 0,\
Age INTEGER DEFAULT 0, 
Jobs TEXT DEFAULT NONE,
'Profile Created Date' INTEGER DEFAULT 0\
"""

GLOBAL_DATA_TABLE = """\
Key TEXT DEFAULT NONE PRIMARY KEY,\
'Key Type' TEXT DEFAULT NONE,\
'Debug Enabled' BOOL DEFAULT FALSE,\
'Is Unstable' BOOL DEFAULT FALSE\
"""

class TWD:
    def __init__(self, GlobalData):
        self.TWDCONNECTION = connect("TWD.db")
        self.Cursor = self.TWDCONNECTION.cursor()
        self._GenerateBase()

    def _GenerateBase(self):
        Cursor = self.Generate_Cursor()
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS Players({PLAYER_TABLE})")
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS 'Global Data'({GLOBAL_DATA_TABLE})")
        self.TWDCONNECTION.commit()
        Cursor.close()

    def Save_Global_Data(self, GlobalData):
        Cursor = self.Generate_Cursor()
        Cursor.execute(f"INSERT OR IGNORE INTO 'Global Data'(Key, 'Key Type', 'Debug Enabled', 'Is Unstable') VALUES(?, ?, ?, ?)",
                            (GlobalData.Key, GlobalData.KeyType, GlobalData.Debug, GlobalData.Unstable))
        self.TWDCONNECTION.commit()
        Cursor.close()

    def Generate_Cursor(self):
        return self.TWDCONNECTION.cursor()
    
    def Load_Players(self, GlobalData):
        JobsSelector = {"Harvest Apples": HarvestApples,
                        "Chop Trees": ChopTrees,
                        "Mine Coal": MineCoal}

        PlayerDataMap = ["UUID", "Username","Nickname","Password",
                         "Experience","Level","Wallet","Health",
                         "Hunger","Thirst","Sanity", "Morale",
                         "Age", "Jobs", "Profile Created Date"]
        Players = {}
        Members = {Member.name: Member for Member in GlobalData.Guilds[0].members}
        Cursor = self.Generate_Cursor()
        PlayerDataList = Cursor.execute("SELECT * FROM Players").fetchall()
        for PlayerData in PlayerDataList:
            PlayerDataMapped = {}
            for Index, Data in enumerate(PlayerData):
                PlayerDataMapped.update({PlayerDataMap[Index]:Data})
            LoadedPlayer = Player(Members[PlayerData[1]])
            for Name, Attribute in LoadedPlayer.Profile.items():
                if Name not in ["Member Object", "Jobs"]:
                    LoadedPlayer.Profile[Name] = PlayerDataMapped[Name]
                if Name == "Jobs":
                    Jobs = PlayerDataMapped[Name].split(",")
                    for Job in Jobs:
                        LoadedPlayer.Profile[Name].update({Job: JobsSelector[Job]()})
            Players.update({LoadedPlayer.Profile["UUID"]:LoadedPlayer})
        self.TWDCONNECTION.commit()
        Cursor.close()
        return Players

    # def Check_New_Players(self, GlobalData):
    #     for Player in GlobalData.FoundMembers.values():
    #         self.Cursor.execute(f"INSERT OR IGNORE INTO Players(UUID, Username, Nickname) VALUES(?, ?, ?)",
    #                             (Player.UUID, Player.Name, Player.Nickname))
    #     self.TWDCONNECTION.commit()