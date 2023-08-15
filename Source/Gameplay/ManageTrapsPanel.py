from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

from WarningMessage import Warning_Message

class ManageTrapsPanel:
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
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Manage Traps Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        self.SelectionBaitOptions = [SelectOption(label="Common Bait", description=self.Player.Baits["Common Bait"]),
                                     SelectOption(label="Rare Bait", description=self.Player.Baits["Rare Bait"]),
                                     SelectOption(label="Elite Bait", description=self.Player.Baits["Elite Bait"]),
                                     SelectOption(label="Legendary Bait", description=self.Player.Baits["Legendary Bait"]),
                                     SelectOption(label="Fabled Bait", description=self.Player.Baits["Fabled Bait"]),
                                     SelectOption(label="Divine Bait", description=self.Player.Baits["Divine Bait"]),
        ]
        self.SelectionEnclosureOptions = [SelectOption(label="Tiny Net", description=self.Player.Enclosures["Tiny Nets"]),
                                          SelectOption(label="Small Net", description=self.Player.Enclosures["Small Nets"]),
                                          SelectOption(label="Medium Net", description=self.Player.Enclosures["Medium Nets"]),
                                          SelectOption(label="Large Net", description=self.Player.Enclosures["Large Nets"]),
                                          SelectOption(label="Enormous Net", description=self.Player.Enclosures["Enormous Nets"]),
                                          SelectOption(label="Tiny Aquatic Net", description=self.Player.Enclosures["Tiny Aquatic Nets"]),
                                          SelectOption(label="Small Aquatic Net", description=self.Player.Enclosures["Small Aquatic Nets"]),
                                          SelectOption(label="Medium Aquatic Net", description=self.Player.Enclosures["Medium Aquatic Nets"]),
                                          SelectOption(label="Large Aquatic Net", description=self.Player.Enclosures["Large Aquatic Nets"]),
                                          SelectOption(label="Enormous Aquatic Net", description=self.Player.Enclosures["Enormous Aquatic Nets"]),
                                          SelectOption(label="Tiny Cage", description=self.Player.Enclosures["Tiny Cages"]),
                                          SelectOption(label="Small Cage", description=self.Player.Enclosures["Small Cages"]),
                                          SelectOption(label="Medium Cage", description=self.Player.Enclosures["Medium Cages"]),
                                          SelectOption(label="Large Cage", description=self.Player.Enclosures["Large Cages"]),
                                          SelectOption(label="Enormous Cage", description=self.Player.Enclosures["Enormous Cages"]),
        ]
        
        self.BaitSelection = Select(placeholder="Select Bait", options=self.SelectionBaitOptions)
        self.EnclosureSelection = Select(placeholder="Select Enclosure", options=self.SelectionEnclosureOptions)
        self.CreatureCollectingPanelReturnButton = Button(label="Return to Creature Collecting Panel", style=ButtonStyle.red)

        self.CreatureCollectingPanelReturnButton.callback = self.CreatureCollectingPanel.Reset

        self.BaseViewFrame.add_item(self.BaitSelection)
        self.BaseViewFrame.add_item(self.EnclosureSelection)
        self.BaseViewFrame.add_item(self.CreatureCollectingPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)