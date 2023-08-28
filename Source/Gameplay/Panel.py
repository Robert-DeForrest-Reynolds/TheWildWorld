# This is an abstract base class

from discord import errors, Embed
from discord.ui import View

class Panel:
    def __init__(self, Context, Player, GlobalData):
        self.Context = Context
        self.Player = Player
        self.GlobalData = GlobalData
        
    def Clear(self):
        self.ViewFrame.clear_items()
        self.EmbedFrame.clear_fields()

    async def TimeoutDelete(self):
        try:
            self.Player.PanelOn = False
            try:
                await self.PanelMessage.delete()
            except:
                print("Failed to delete panel message for some reason")
            try:
                self.GlobalData.PlayerPanels.pop(self.Player.Profile["UUID"])
            except:
                print("Failed to pop player for some reason.")
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