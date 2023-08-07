from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

class CreatureCollectingPanel:
    def __init__(self, Context, Player, GivenInteraction, PlayerPetsPanel, GlobalData):
        self.Context = Context
        self.Player = Player
        self.GivenInteraction = GivenInteraction
        self.GlobalData = GlobalData
        self.PlayerPetsPanel = PlayerPetsPanel
        create_task(self.Construct_Panel())

    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Creature Collecting Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        self.SelectionOptions = [SelectOption(label="Manage Bait", description="Craft and buy baits."),
                                 SelectOption(label="Manage Enclosure", description="Craft and buy enclosures."),
                                 SelectOption(label="Manage Traps", description="Craft, place and monitor traps."),
        ]
        
        self.Selection = Select(placeholder="Collecting Actions", options=self.SelectionOptions)
        self.PetsPanelReturnButton = Button(label="Return to Pets Panel", style=ButtonStyle.red)

        self.PetsPanelReturnButton.callback = self.PlayerPetsPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.PetsPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)