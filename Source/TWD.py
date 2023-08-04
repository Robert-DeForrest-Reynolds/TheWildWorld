from sqlite3 import connect
from asyncio import create_task

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
Jobs BLOB DEFAULT NONE\
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
        self.Cursor.execute(f"CREATE TABLE IF NOT EXISTS Players({PLAYER_TABLE})")
        self.Cursor.execute(f"CREATE TABLE IF NOT EXISTS 'Global Data'({GLOBAL_DATA_TABLE})")
        self.TWDCONNECTION.commit()
        Cursor.close()

    def Save_Global_Data(self, GlobalData):
        self.Cursor.execute(f"INSERT OR IGNORE INTO 'Global Data'(Key, 'Key Type', 'Debug Enabled', 'Is Unstable') VALUES(?, ?, ?, ?)",
                            (GlobalData.Key, GlobalData.KeyType, GlobalData.Debug, GlobalData.Unstable))
        self.TWDCONNECTION.commit()

    def Generate_Cursor(self):
        return self.TWDCONNECTION.cursor()
    

    # def Check_New_Players(self, GlobalData):
    #     for Player in GlobalData.FoundMembers.values():
    #         self.Cursor.execute(f"INSERT OR IGNORE INTO Players(UUID, Username, Nickname) VALUES(?, ?, ?)",
    #                             (Player.UUID, Player.Name, Player.Nickname))
    #     self.TWDCONNECTION.commit()