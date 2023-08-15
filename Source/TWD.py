from sqlite3 import connect
from asyncio import create_task
from PlayerObject import PlayerObject
from Jobs.HarvestApples import HarvestApples
from Jobs.ChopOakTrees import ChopOakTrees
from Jobs.MineCoal import MineCoal

### Key Notes ###
# - We NEVER save ALL players at once, or with any central function.
#   ALL player data is to be edited, and saved individually throughout the bot's life

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
ProfileCreationDate INTEGER DEFAULT 0\
"""

GLOBAL_DATA_TABLE = """\
Key TEXT DEFAULT NONE PRIMARY KEY,\
KeyType TEXT DEFAULT NONE,\
DebugEnabled BOOL DEFAULT FALSE,\
IsUnstable BOOL DEFAULT FALSE,\
DayCount INTEGER DEFAULT 0\
"""

JOBS_TABLE = """\
JobUUID INTEGER DEFAULT NONE PRIMARY KEY,\
OwnerUUID INTEGER DEFAULT NONE,\
Name TEXT DEFAULT NONE,\
TerminationDate INTEGER DEFAULT NONE
"""

class TWD:
    def __init__(self, GlobalData):
        self.TWDCONNECTION = connect("TWD.db")
        self.Cursor = self.TWDCONNECTION.cursor()
        self._Generate_Base()

    def _Generate_Base(self):
        Cursor = self.Generate_Cursor()
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS Players({PLAYER_TABLE})")
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS GlobalData({GLOBAL_DATA_TABLE})")
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS Jobs({JOBS_TABLE})")
        self.TWDCONNECTION.commit()
        Cursor.close()

    def Save_Global_Data(self, GlobalData):
        Cursor = self.Generate_Cursor()
        Cursor.execute(f"INSERT OR IGNORE INTO GlobalData(Key, KeyType, DebugEnabled, IsUnstable) VALUES(?, ?, ?, ?)",
                       (GlobalData.Key, GlobalData.KeyType, GlobalData.Debug, GlobalData.Unstable))
        self.TWDCONNECTION.commit()
        Cursor.close()

    def Generate_Cursor(self):
        return self.TWDCONNECTION.cursor()
    
    def Load_Players(self, GlobalData):
        PlayerDataMap = ["UUID", "Username","Nickname","Password",
                         "Experience","Level","Wallet","Health",
                         "Hunger","Thirst","Sanity", "Morale",
                         "Age", "ProfileCreationDate"]
        Players = {}
        Cursor = self.Generate_Cursor()
        PlayerList = Cursor.execute("SELECT * FROM Players").fetchall()
        for Player in PlayerList:
            PlayerDataMapped = {}
            for Index, Data in enumerate(Player):
                PlayerDataMapped.update({PlayerDataMap[Index]:Data})
            LoadedPlayer = PlayerObject(GlobalData.Members[Player[1]])
            LoadedPlayer.Password = PlayerDataMapped["Password"]
            LoadedPlayer.ProfileCreationDate = PlayerDataMapped["ProfileCreationDate"]
            for Name, Attribute in LoadedPlayer.Profile.items():
                LoadedPlayer.Profile[Name] = PlayerDataMapped[Name]
            Players.update({LoadedPlayer.Profile["UUID"]:LoadedPlayer})
        self.TWDCONNECTION.commit()
        Cursor.close()
        return Players
    
    def Load_Player_Jobs():
        pass

    # def Check_New_Players(self, GlobalData):
    #     for Player in GlobalData.FoundMembers.values():
    #         self.Cursor.execute(f"INSERT OR IGNORE INTO Players(UUID, Username, Nickname) VALUES(?, ?, ?)",
    #                             (Player.UUID, Player.Name, Player.Nickname))
    #     self.TWDCONNECTION.commit()