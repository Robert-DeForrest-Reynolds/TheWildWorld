from discord import SelectOption, Embed, ButtonStyle
from discord.ui import Select, Button, View

from asyncio import create_task

class WorkPanel:
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalData):
        self.Context = Context
        self.Player = Player
        self.GivenInteraction = GivenInteraction
        self.GlobalData = GlobalData
        self.PlayerPlayPanel = PlayerPlayPanel
        create_task(self.Construct_Panel())

    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Work Panel", 
                                description=f"aka {self.Player.Profile['Username']}")

        if len(self.Player.Profile["Jobs"]) >= 1:
            for JobName, JobObject in self.Player.Profile["Jobs"].items():
                self.WorkSelectionOptions = []
                self.WorkSelection = Select(placeholder="What work would you like to do?", 
                                            options=self.WorkSelectionOptions,
                                            custom_id="Work Selection")
                self.WorkSelection.callback = self.Load_Selection
                self.BaseViewFrame.add_item(self.WorkSelection)
                self.WorkSelectionOptions.append(SelectOption(label=JobName, 
                                                              description=JobObject.Description))
        else:
                self.EmbedFrame.add_field(name="You have no job.", value="You should probably go get one.")

        self.PlayPanelReturnButton = Button(label="Return to Play Panel",
                                            style=ButtonStyle.red,
                                            row=4)
        
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.BaseViewFrame.add_item(self.PlayPanelReturnButton)
            
        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)

    async def Load_Selection(self, WorkSelectionInteraction):
        self.WorkSelection = self.Player.Profile['Jobs'][WorkSelectionInteraction.data["values"][0]]
        self.WorkSelection.placeholder = WorkSelectionInteraction.data["values"][0]
        WorkButton = Button(label=self.WorkSelection.Name, custom_id="Work Button")
        WorkButton.callback = self.Work
        if WorkButton not in self.BaseViewFrame.children:
            self.BaseViewFrame.add_item(WorkButton)

        await WorkSelectionInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)

    async def Work(self, ButtonInteraction):
        Result = await self.WorkSelection.Harvest(self.Player)
        if Result[0] == "Cooldown":
            self.EmbedFrame.clear_fields()
            self.EmbedFrame.insert_field_at(0, name="Warning", value=Result[1])
        else:
            self.EmbedFrame.clear_fields()
            self.EmbedFrame.insert_field_at(0, name="Successful Harvest", value=Result[1])
        await ButtonInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)