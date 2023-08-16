# This is an abstract base class

from discord import errors

class Panel:
    async def TimeoutDelete(self):
        try:
            self.Player.PanelOn = False
            await self.PanelMessage.delete()
            self.GlobalData.PlayerPanels.pop(self.Player.Profile["UUID"])
        except errors.NotFound:
            self.GlobalData.Logger.info("Panel already deleted, timeout useless.")

    async def Delete(self):
        self.Player.PanelOn = False
        await self.PanelMessage.delete()