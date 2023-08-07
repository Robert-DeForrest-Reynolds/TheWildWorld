from discord import Embed, ButtonStyle
from discord.ui import View, Button
from asyncio import create_task

from WarningMessage import Warning_Message

class CreatureCollectingPanel:
    def __init__(self, Context, Player, GivenInteraction, PlayerPetsPanel, GlobalData):
        if GivenInteraction.user.id == Context.author.id:
            self.Context = Context
            self.Player = Player
            self.GivenInteraction = GivenInteraction
            self.GlobalData = GlobalData
            self.PlayerPetsPanel = PlayerPetsPanel
            create_task(self.Construct_Panel())
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))

    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Creature Collecting Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        self.PetsPanelReturnButton = Button(label="Return to Pets Panel",
                                            style=ButtonStyle.red,
                                            row=4)

        self.PetsPanelReturnButton.callback = self.PlayerPetsPanel.Reset

        self.BaseViewFrame.add_item(self.PetsPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)