from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task
from WarningMessage import Warning_Message

from Gameplay.CreatureCollectingPanel import CreatureCollectingPanel
from Gameplay.CreatureSanctuaryPanel import CreatureSanctuaryPanel

class PetsPanel:
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
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Pets Panel",
                                description=f"aka {self.Player.Profile['Username']}")
        
        self.SelectionOptions = [SelectOption(label="Creature Collecting", description="Manage your containers and baits for creatures."),
                                 SelectOption(label="Creature Sanctuary", description="Interact with your creatures."),
        ]
        
        self.Selection = Select(placeholder="Pet Actions",
                                options=self.SelectionOptions)
        self.PlayPanelReturnButton = Button(label="Return to Play Panel",
                                            style=ButtonStyle.red,
                                            row=4)

        self.Selection.callback = self.Create_Panel
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.PlayPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)
        
    async def Create_Panel(self, SelectInteraction):
        if SelectInteraction.user.id == self.Context.author.id:
            self.SelectedPanel = SelectInteraction.data['values'][0]
            
            if self.SelectedPanel == "Creature Collecting":
                CreatureCollectingPanel(self.Context,
                                        self.Player,
                                        SelectInteraction,
                                        self,
                                        self.GlobalData)
            elif self.SelectedPanel == "Creature Sanctuary":
                CreatureSanctuaryPanel(self.Context,
                                       self.Player,
                                       SelectInteraction,
                                       self,
                                       self.GlobalData)
        
        
    async def Reset(self, ButtonInteraction):
        if ButtonInteraction.user.id == self.Context.author.id:
            self.GivenInteraction = ButtonInteraction
            await self.Construct_Panel()
        