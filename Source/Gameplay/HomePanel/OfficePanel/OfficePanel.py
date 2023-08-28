from discord import Embed, ButtonStyle
from discord.ui import View, Button

from asyncio import create_task

from Gameplay.Panel import Panel

from WarningMessage import Warning_Message

class OfficePanel(Panel):
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalData):
        if GivenInteraction.user.id == Context.author.id:
            super().__init__(Context, Player, GlobalData)
            self.PlayerPlayPanel = PlayerPlayPanel
            create_task(self.Construct_Panel(GivenInteraction))
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))

    async def Construct_Panel(self, GivenInteraction):
        self.Clear()
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Office Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        self.PlayPanelReturnButton = Button(label="Return to Play Panel",
                                            style=ButtonStyle.red,
                                            row=4)

        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.ViewFrame.add_item(self.PlayPanelReturnButton)

        await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)