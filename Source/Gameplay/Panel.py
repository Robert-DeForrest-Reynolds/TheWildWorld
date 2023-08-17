# This is an abstract base class

from discord import errors, Embed
from discord.ui import View

class Panel:
    def __init__(self, Context, Player, GlobalData):
        self.BaseViewFrame = View(timeout=12)
        self.EmbedFrame = Embed()
        self.BaseViewFrame.on_timeout = self.TimeoutDelete
        self.Context = Context
        self.Player = Player
        self.GlobalData = GlobalData

    async def TimeoutDelete(self):
        try:
            self.Player.PanelOn = False
            try:
                await self.PanelMessage.delete()
            except:
                print("Failed to delete panel message for some reason")
            self.GlobalData.PlayerPanels.pop(self.Player.Profile["UUID"])
        except errors.NotFound:
            self.GlobalData.Logger.info("Panel already deleted, timeout useless.")

    async def Delete(self):
        self.Player.PanelOn = False
        try:
            await self.PanelMessage.delete()
        except:
            print("Failed to delete panel message for some reason")

    async def Reset(self, ButtonInteraction):
        if ButtonInteraction.user.id == self.Context.author.id:
            await self.Construct_Panel(ButtonInteraction)
    
    async def Cleanup(self):
        if len(self.BaseViewFrame.children) >= 1:
            self.BaseViewFrame.clear_items()