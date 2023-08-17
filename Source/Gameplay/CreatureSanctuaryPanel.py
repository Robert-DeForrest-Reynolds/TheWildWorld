from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select

from asyncio import create_task

from Gameplay.Panel import Panel

from WarningMessage import Warning_Message

class CreatureSanctuaryPanel(Panel):
    def __init__(self, Context, Player, GivenInteraction, PlayerPetsPanel, GlobalData):
        if GivenInteraction.user.id == Context.author.id:
            super().__init__(Context, Player, GlobalData)
            self.PlayerPetsPanel = PlayerPetsPanel
            create_task(self.Construct_Panel(GivenInteraction))
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))

    async def Construct_Panel(self, GivenInteraction):
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Creature Sanctuary Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        self.PetsPanelReturnButton = Button(label="Return to Pets Panel",
                                            style=ButtonStyle.red,
                                            row=4)

        self.PetsPanelReturnButton.callback = self.PlayerPetsPanel.Reset

        self.BaseViewFrame.add_item(self.PetsPanelReturnButton)

        await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)