from asyncio import create_task, sleep
from time import time

class WorldSimulation:
    def __init__(self, GlobalData):
        self.GlobalData = GlobalData
        create_task(self.Initialize_Simulation())

    def Load_Day_Count(self):
        Cursor = self.GlobalData.Database.Generate_Cursor()
                                       # This quotes vs double quotes thing in Python's Sqlite3 library is fucking dumb.
                                       # I'm sorry to hurt whoever's feelings. But this is genuinely infuriating.
        self.DayCount = Cursor.execute("SELECT DayCount FROM GlobalData").fetchone()[0]
        Cursor.close()

    async def Initialize_Simulation(self):
        self.Load_Day_Count()

        # Days are currently 32 minutes long, leaving 45 in-game days in a day in reality. This is 1920 seconds.
        while True:
            await sleep(1920)
            self.DayCount += 1
            await self.Expire_Jobs()
            await self.GlobalData.Channels["town-hall"].send(f"It is now day {self.DayCount}! The Hold wishes everyone success!")
            Cursor = self.GlobalData.Database.Generate_Cursor()
            Cursor.execute("UPDATE GlobalData SET DayCount = ?", (self.DayCount,))
            self.GlobalData.Database.TWDCONNECTION.commit()
            Cursor.close()
            self.GlobalData.Logger.info(f"It is now day {self.DayCount}")


    async def Expire_Jobs(self):
        Checktime = time()
        for Player in self.GlobalData.Players.values():
            PlayerJobs = {Job.Name:Job for Job in Player.Profile["Jobs"].values()}
            for Job in PlayerJobs.values():
                print(Checktime)
                print(Job.TerminationDate)
                if Job.TerminationDate <= Checktime:
                    print(Player.Profile["Jobs"])
                    Player.Profile["Jobs"].pop(Job.Name)
                    print(Player.Profile["Jobs"])
                    print("Job terminated")
