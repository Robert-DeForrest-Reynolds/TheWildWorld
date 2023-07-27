from sqlite3 import connect
from asyncio import create_task

PLAYER_TABLE = """\
UUID INTEGER DEFAULT 0 PRIMARY KEY,\
Username TEXT DEFAULT NONE,\
Nickname TEXT DEFAULT NONE,\
Experience INTEGER DEFAULT 0,\
Level INTEGER DEFAULT 1,\
Wallet INTEGER DEFAULT 0,\
Health INTEGER DEFAULT 5000,\
Hunger INTEGER DEFAULT 0,\
Thirst INTEGER DEFAULT 0,\
Sanity INTEGER DEFAULT 0,\
Jobs BLOB DEFAULT NONE\
"""

class TWD:
    def __init__(self, GlobalData):
        self.TWD_CONNECTION = connect("TWD.db")
        self.Cursor = self.TWD_CONNECTION.cursor()
        self._GenerateBase()
        self._Check_New_Players(GlobalData)

    def _GenerateBase(self):
        self.Cursor.execute(f"CREATE TABLE IF NOT EXISTS Players({PLAYER_TABLE})")

    def _Check_New_Players(self, GlobalData):
        for Player in GlobalData.LeviMembers.values():
            self.Cursor.execute(f"INSERT OR IGNORE INTO Players(UUID, Username, Nickname) VALUES(?, ?, ?)", (Player.UUID, Player.Name, Player.Nickname))
        self.TWD_CONNECTION.commit()