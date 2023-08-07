from asyncio import create_task, sleep

class WorldSimulation:
    def __init__(self, GlobalData):
        self.GlobalData = GlobalData
        create_task(self.Initialize_Simulation())

    async def Initialize_Simulation(self):
        self.DayCount = 1

        # Days are currently 32 minutes long, leaving 45 in-game days in a day in reality. This is 1920 seconds.
        while True:
            await sleep(1920)
            self.DayCount += 1
            await self.GlobalData.Channels["town-hall"].send(f"It is now day {self.DayCount}! The Hold wishes everyone success!")
            self.GlobalData.Logger.info(f"It is now day {self.DayCount}")
