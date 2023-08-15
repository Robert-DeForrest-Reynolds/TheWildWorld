from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

from Objects.Trap import Trap

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
    
        self.BitSelectMenuOptions = [SelectOption(label="Common Bait", description=self.Player.Baits["Common Bait"]),
                                     SelectOption(label="Rare Bait", description=self.Player.Baits["Rare Bait"]),
                                     SelectOption(label="Elite Bait", description=self.Player.Baits["Elite Bait"]),
                                     SelectOption(label="Legendary Bait", description=self.Player.Baits["Legendary Bait"]),
                                     SelectOption(label="Fabled Bait", description=self.Player.Baits["Fabled Bait"]),
                                     SelectOption(label="Divine Bait", description=self.Player.Baits["Divine Bait"]),
        ]
        self.EnclosureSelectMenuOptions = [SelectOption(label="Nets", description=self.Player.Enclosures["Nets"]),
                                          SelectOption(label="Nets", description=self.Player.Enclosures["Aquatic Nets"]),
                                          SelectOption(label="Small Cage", description=self.Player.Enclosures["Small Cages"]),
                                          SelectOption(label="Large Cage", description=self.Player.Enclosures["Large Cages"]),
                                          SelectOption(label="Enormous Cage", description=self.Player.Enclosures["Enormous Cages"]),
        ]
        
        self.BaitSelectMenu = Select(placeholder="Select Bait", options=self.BitSelectMenuOptions)
        self.EnclosureSelectMenu = Select(placeholder="Select Enclosure", options=self.EnclosureSelectMenuOptions)
        self.LayTrapButton = Button(label="Lay Trap", style=ButtonStyle.blurple, row=2)
        self.CreatureCollectingPanelReturnButton = Button(label="Return to Creature Collecting Panel", style=ButtonStyle.red, row=4)

        self.BaitSelectMenu.callback = self.Select_Bait
        self.EnclosureSelectMenu.callback = self.Select_Enclosure
        self.LayTrapButton.callback = self.Lay_Trap
        self.CreatureCollectingPanelReturnButton.callback = self.CreatureCollectingPanel.Reset

        self.BaseViewFrame.add_item(self.BaitSelectMenu)
        self.BaseViewFrame.add_item(self.EnclosureSelectMenu)
        self.BaseViewFrame.add_item(self.LayTrapButton)
        self.BaseViewFrame.add_item(self.CreatureCollectingPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)
        
    async def Select_Bait(self, SelectInteraction):
        self.SelectedBait = SelectInteraction.data["values"][0]
        self.BaitSelectMenu.placeholder = self.SelectedBait

        await SelectInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)

    async def Select_Enclosure(self, SelectInteraction):
        self.SelectedEnclosure = SelectInteraction.data["values"][0]
        self.EnclosureSelectMenu.placeholder = self.SelectedEnclosure
        
        await SelectInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)
        
    async def Lay_Trap(self, ButtonInteraction):
        self.Player.Traps.update({f"{self.SelectedBait} - {self.SelectedEnclosure}" : Trap(f"{self.SelectedBait} - {self.SelectedEnclosure}")})
        print(self.Player.Traps)
        self.EmbedFrame.clear_fields()
        self.EmbedFrame.add_field(name="Successfully laid trap", value=f"Trap laid: {self.SelectedBait} - {self.SelectedEnclosure}")
        await ButtonInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)