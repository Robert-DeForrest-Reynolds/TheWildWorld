from discord import SelectOption, Embed, ButtonStyle
from discord.ui import Select, Button, View

from asyncio import create_task

class WorkPanel:
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalDataRef):
        self.Context = Context
        self.Player = Player
        self.GivenInteraction = GivenInteraction
        self.GlobalDataRef = GlobalDataRef
        self.PlayerPlayPanel = PlayerPlayPanel
        create_task(self.Construct_Panel())

    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Nickname}'s Work Panel", description=f"aka {self.Player.Name}")

        if len(self.Player.Jobs) >= 1:
            for WorkType in self.Player.Jobs:
                self.WorkSelectionOptions = []
                self.WorkSelection = Select(placeholder="What work would you like to do?", options=self.WorkSelectionOptions)
                self.WorkSelection.callback = self.Load_Selection
                self.BaseViewFrame.add_item(self.WorkSelection)
                self.WorkSelectionOptions.append(SelectOption(label=WorkType.Name, description=""))
        else:
                self.EmbedFrame.add_field(name="You have no job.", value="You should probably go get one.")

        self.PlayPanelReturnButton = Button(label="Return to Play Panel", style=ButtonStyle.red)
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset
        self.BaseViewFrame.add_item(self.PlayPanelReturnButton)
        
            
        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)

    async def Load_Selection(self, WorkSelectionInteraction):
        WorkSelection = WorkSelectionInteraction.data["values"][0]
        self.WorkSelection.placeholder = WorkSelectionInteraction.data["values"][0]
        WorkButton = Button(label=f"")

    async def Return_To_MainPanel():
        pass