from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

from WarningMessage import Warning_Message

class ManageBaitPanel:
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
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Manage Bait Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        # Tiny = Insect
        # Small = Mouse to Bobcat
        # Medium = Tiger to Bear
        # Large = Hippo to Elephant
        # Enoumous = Whale
        self.EmbedFrame.add_field(name="Tiny Nets", value=self.Player.Enclosures["Tiny Nets"])
        self.EmbedFrame.add_field(name="Small Nets", value=self.Player.Enclosures["Small Nets"])
        self.EmbedFrame.add_field(name="Medium Nets", value=self.Player.Enclosures["Medium Nets"])
        self.EmbedFrame.add_field(name="Large Nets", value=self.Player.Enclosures["Large Nets"])
        self.EmbedFrame.add_field(name="Enourmous Nets", value=self.Player.Enclosures["Enourmous Nets"])
        self.EmbedFrame.add_field(name="Tiny Aquatic Nets", value=self.Player.Enclosures["Tiny Aquatic Nets"])
        self.EmbedFrame.add_field(name="Small Aquatic Nets", value=self.Player.Enclosures["Small Aquatic Nets"])
        self.EmbedFrame.add_field(name="Medium Aquatic Nets", value=self.Player.Enclosures["Medium Aquatic Nets"])
        self.EmbedFrame.add_field(name="Large Aquatic Nets", value=self.Player.Enclosures["Large Aquatic Nets"])
        self.EmbedFrame.add_field(name="Enourmous Aquatic Nets", value=self.Player.Enclosures["Enourmous Aquatic Nets"])
        self.EmbedFrame.add_field(name="Tiny Cages", value=self.Player.Enclosures["Tiny Cages"])
        self.EmbedFrame.add_field(name="Small Cages", value=self.Player.Enclosures["Small Cages"])
        self.EmbedFrame.add_field(name="Medium Cages", value=self.Player.Enclosures["Medium Cages"])
        self.EmbedFrame.add_field(name="Large Cages", value=self.Player.Enclosures["Large Cages"])
        self.EmbedFrame.add_field(name="Enourmous Cages", value=self.Player.Enclosures["Enourmous Cages"])

        self.SelectionOptions = [SelectOption(label="Buy Enclosure", description="Buy enclosures from the player market."),
                                 SelectOption(label="Craft Enclosure", description="Craft enclosures with your own materials."),
        ]
        
        self.Selection = Select(placeholder="Collecting Actions", options=self.SelectionOptions)
        self.PetsPanelReturnButton = Button(label="Return to Pets Panel", style=ButtonStyle.red)

        self.PetsPanelReturnButton.callback = self.PlayerPetsPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.PetsPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)