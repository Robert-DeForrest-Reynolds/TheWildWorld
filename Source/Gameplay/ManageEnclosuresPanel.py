from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

from WarningMessage import Warning_Message

class ManageEnclosuresPanel:
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
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Manage Enclosures Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        # Tiny = Insect
        # Small = Mouse to Bobcat
        # Medium = Tiger to Bear
        # Large = Hippo to Elephant
        # Enoumous = Whale
        self.EmbedFrame.add_field(name="Nets", value=self.Player.Enclosures["Nets"])
        self.EmbedFrame.add_field(name="Aquatic Nets", value=self.Player.Enclosures["Aquatic Nets"])
        self.EmbedFrame.add_field(name="", value="", inline=False)
        
        self.EmbedFrame.add_field(name="Small Cages", value=self.Player.Enclosures["Small Cages"])
        self.EmbedFrame.add_field(name="Large Cages", value=self.Player.Enclosures["Large Cages"])
        self.EmbedFrame.add_field(name="", value="", inline=False)
        
        self.EmbedFrame.add_field(name="Enormous Cages", value=self.Player.Enclosures["Enormous Cages"])

        self.SelectionOptions = [SelectOption(label="Buy Enclosure", description="Buy enclosures from the player market."),
                                 SelectOption(label="Craft Enclosure", description="Craft enclosures with your own materials."),
        ]
        
        self.Selection = Select(placeholder="Enclosure Actions", options=self.SelectionOptions)
        self.CreatureCollectingPanelReturnButton = Button(label="Return to Creature Collecting Panel", style=ButtonStyle.red)

        self.CreatureCollectingPanelReturnButton.callback = self.CreatureCollectingPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.CreatureCollectingPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)