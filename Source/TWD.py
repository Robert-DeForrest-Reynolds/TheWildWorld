from sqlite3 import connect
from asyncio import create_task
from PlayerObject import PlayerObject
from Jobs.Job import Job
from Jobs.HarvestApples import HarvestApples
from Jobs.ChopOakTrees import ChopOakTrees
from Jobs.MineCoal import MineCoal
from Tools.JobsSelector import JobsSelector

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
Health INTEGER DEFAULT 20,\
Hunger INTEGER DEFAULT 0,\
Thirst INTEGER DEFAULT 0,\
Sanity INTEGER DEFAULT 0,\
Morale INTEGER DEFAULT 0,\
Age INTEGER DEFAULT 0, 
ProfileCreationDate INTEGER DEFAULT 0,\
Inventory TEXT DEFAULT NONE
"""

GLOBAL_DATA_TABLE = """\
Key TEXT DEFAULT NONE PRIMARY KEY,\
KeyType TEXT DEFAULT NONE,\
DebugEnabled BOOL DEFAULT FALSE,\
IsUnstable BOOL DEFAULT FALSE,\
DayCount INTEGER DEFAULT 0\
"""

JOBS_TABLE = """\
JobUUID BLOG DEFAULT NONE PRIMARY KEY,\
OwnerUUID INTEGER DEFAULT NONE,\
Name TEXT DEFAULT NONE,\
TerminationDate INTEGER DEFAULT NONE,\
HarvestDate INTEGER DEFAULT NONE\
"""

class TWD:
    def __init__(self, GlobalData):
        self.TWDCONNECTION = connect("TWD.db")
        self.Cursor = self.TWDCONNECTION.cursor()
        self.GlobalData = GlobalData
        self._Generate_Base()

    def _Generate_Base(self):
        Cursor = self.Generate_Cursor()
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS Players({PLAYER_TABLE})")
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS GlobalData({GLOBAL_DATA_TABLE})")
        Cursor.execute(f"CREATE TABLE IF NOT EXISTS Jobs({JOBS_TABLE})")
        self.TWDCONNECTION.commit()
        Cursor.close()

    def Save_Global_Data(self):
        Cursor = self.Generate_Cursor()
        Cursor.execute(f"INSERT OR IGNORE INTO GlobalData(Key, KeyType, DebugEnabled, IsUnstable) VALUES(?, ?, ?, ?)",
                       (self.GlobalData.Key, self.GlobalData.KeyType, self.GlobalData.Debug, self.GlobalData.Unstable))
        self.TWDCONNECTION.commit()
        Cursor.close()

    def Generate_Cursor(self):
        return self.TWDCONNECTION.cursor()
    
    def Load_Players(self):
        Mapping = ["UUID", "Username","Nickname","Password",
                   "Experience","Level","Wallet","Health",
                   "Hunger","Thirst","Sanity", "Morale",
                   "Age", "ProfileCreationDate"]
        Players = {}
        Cursor = self.Generate_Cursor()
        PlayerData = Cursor.execute("SELECT * FROM Players").fetchall()
        for Player in PlayerData:
            PlayDataMapped = {}
            for Index, Data in enumerate(Player):
                PlayDataMapped.update({Mapping[Index]:Data})
            LoadedPlayer = PlayerObject(self.GlobalData.Members[Player[1]])
            LoadedPlayer.Password = PlayDataMapped["Password"]
            LoadedPlayer.ProfileCreationDate = PlayDataMapped["ProfileCreationDate"]
            for Name, Attribute in LoadedPlayer.Profile.items():
                LoadedPlayer.Profile[Name] = PlayDataMapped[Name]
            Players.update({LoadedPlayer.Profile["UUID"]:LoadedPlayer})
        self.TWDCONNECTION.commit()
        Cursor.close()
        return Players
    
    def Load_Player_Jobs(self):
        Mapping = ["JobUUID", "OwnerUUID", "Name", "TerminationDate", "HarvestDate"]
        Cursor = self.Generate_Cursor()
        JobsData = Cursor.execute("SELECT * FROM JOBS")
        for JobData in JobsData:
            JobDataMapped = {}
            for Index, Data in enumerate(JobData):
                JobDataMapped.update({Mapping[Index]:Data})
            TempJobObject = JobsSelector[JobDataMapped["Name"]]()
            TempJobObject.UUID = JobDataMapped["JobUUID"]
            TempJobObject.OwnerUUID = JobDataMapped["OwnerUUID"]
            TempJobObject.TerminationDate = JobDataMapped["TerminationDate"]
            TempJobObject.TerminationDate = JobDataMapped["HarvestDate"]
            Player = self.GlobalData.Players[JobDataMapped["OwnerUUID"]]
            Player.Jobs.update({TempJobObject.Name:TempJobObject})
        Cursor.close()

    # def Check_New_Players(self, GlobalData):
    #     for Player in GlobalData.FoundMembers.values():
    #         self.Cursor.execute(f"INSERT OR IGNORE INTO Players(UUID, Username, Nickname) VALUES(?, ?, ?)",
    #                             (Player.UUID, Player.Name, Player.Nickname))
    #     self.TWDCONNECTION.commit()