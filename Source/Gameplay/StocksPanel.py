from discord import Embed, ButtonStyle
from discord.ui import View, Button
from asyncio import create_task
from WarningMessage import Warning_Message

class StocksPanel:
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalData):
        if GivenInteraction.user.id == Context.author.id:
            self.Context = Context
            self.Player = Player
            self.GivenInteraction = GivenInteraction
            self.GlobalData = GlobalData
            self.PlayerPlayPanel = PlayerPlayPanel
            create_task(self.Construct_Panel())
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))

    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Stocks Panel", description=f"aka {self.Player.Profile['Username']}")
    
        self.PlayPanelReturnButton = Button(label="Return to Play Panel", style=ButtonStyle.red)

        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.BaseViewFrame.add_item(self.PlayPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)