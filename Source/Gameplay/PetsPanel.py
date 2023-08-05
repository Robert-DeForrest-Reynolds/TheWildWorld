from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from asyncio import create_task

class PetsPanel:
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalDataRef):
        self.Context = Context
        self.Player = Player
        self.GivenInteraction = GivenInteraction
        self.GlobalDataRef = GlobalDataRef
        self.PlayerPlayPanel = PlayerPlayPanel
        create_task(self.Construct_Panel())

    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Nickname}'s Pets Panel", description=f"aka {self.Player.Name}")
        
        self.SelectionOptions = [SelectOption(label="Bait", description="Manage your bait."),
                                 SelectOption(label="Work", description="Get to work!"),
                                 SelectOption(label="Household", description="Take care of your household; your home, family, personal assets & more."),
                                 SelectOption(label="Pets", description="Take care of some creatures. Some cute, some not."),
                                 SelectOption(label="Market", description="Trade things with other players."),
                                 SelectOption(label="Office", description="Manage your businesses."),
                                 SelectOption(label="Stocks", description="Invest in the public stocks"),
                                 SelectOption(label="The Hold", description="Interact with The Hold, TWW's official Government.")
        ]
        
        self.Selection = Select(placeholder="Pet Actions", options=self.SelectionOptions)
        self.PlayPanelReturnButton = Button(label="Return to Play Panel", style=ButtonStyle.red)

        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.PlayPanelReturnButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)