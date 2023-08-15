from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

from Gameplay.ManageBaitsPanel import ManageBaitsPanel
from Gameplay.ManageEnclosuresPanel import ManageEnclosuresPanel
from Gameplay.ManageTrapsPanel import ManageTrapsPanel

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
    
        self.SelectionOptions = [SelectOption(label="Manage Baits", description="Craft and buy baits."),
                                 SelectOption(label="Manage Enclosures", description="Craft and buy enclosures."),
                                 SelectOption(label="Manage Traps", description="Craft, place and monitor traps."),
        ]
        
        self.Selection = Select(placeholder="Creature Collecting Actions", options=self.SelectionOptions)
        self.PetsPanelReturnButton = Button(label="Return to Pets Panel", style=ButtonStyle.red)

        self.Selection.callback = self.Create_Panel
        self.PetsPanelReturnButton.callback = self.PlayerPetsPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.PetsPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)
        
        
    async def Create_Panel(self, SelectInteraction):
        if SelectInteraction.user.id == self.Context.author.id:
            self.SelectedPanel = SelectInteraction.data['values'][0]
            
            if self.SelectedPanel == "Manage Baits":
                ManageBaitsPanel(self.Context,
                                        self.Player,
                                        SelectInteraction,
                                        self,
                                        self.GlobalData)
            elif self.SelectedPanel == "Manage Enclosures":
                ManageEnclosuresPanel(self.Context,
                                        self.Player,
                                        SelectInteraction,
                                        self,
                                        self.GlobalData)
            elif self.SelectedPanel == "Manage Traps":
                ManageTrapsPanel(self.Context,
                                        self.Player,
                                        SelectInteraction,
                                        self,
                                        self.GlobalData)
                
                
    async def Reset(self, ButtonInteraction):
        if ButtonInteraction.user.id == self.Context.author.id:
            self.GivenInteraction = ButtonInteraction
            await self.Construct_Panel()