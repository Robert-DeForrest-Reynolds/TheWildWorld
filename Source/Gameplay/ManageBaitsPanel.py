from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

from WarningMessage import Warning_Message

class ManageBaitsPanel:
    def __init__(self, Context, Player, GivenInteraction, CreatureCollectingPanel, GlobalData):
        if GivenInteraction.user.id == Context.author.id:
            self.Context = Context
            self.Player = Player
            self.GivenInteraction = GivenInteraction
            self.GlobalData = GlobalData
            self.CreatureCollectingPanel = CreatureCollectingPanel
            create_task(self.Construct_Panel())
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))


    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Manage Baits Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        self.EmbedFrame.add_field(name="Common Bait", value=self.Player.Baits["Common Bait"])
        self.EmbedFrame.add_field(name="Rare Bait", value=self.Player.Baits["Rare Bait"])
        self.EmbedFrame.add_field(name="", value="", inline=False)
        
        self.EmbedFrame.add_field(name="Elite Bait", value=self.Player.Baits["Elite Bait"])
        self.EmbedFrame.add_field(name="Legendary Bait", value=self.Player.Baits["Legendary Bait"])
        self.EmbedFrame.add_field(name="", value="", inline=False)
        
        self.EmbedFrame.add_field(name="Fabled Bait", value=self.Player.Baits["Fabled Bait"])
        self.EmbedFrame.add_field(name="Divine Bait", value=self.Player.Baits["Divine Bait"])

        self.SelectionOptions = [SelectOption(label="Buy Bait", description="Buy baits from the player market."),
                                 SelectOption(label="Craft Bait", description="Craft baits with your own materials."),
        ]
        
        self.Selection = Select(placeholder="Bait Actions", options=self.SelectionOptions)
        self.CreatureCollectingPanelReturnButton = Button(label="Return to Creature Collecting Panel", style=ButtonStyle.red)

        self.CreatureCollectingPanelReturnButton.callback = self.CreatureCollectingPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.CreatureCollectingPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)