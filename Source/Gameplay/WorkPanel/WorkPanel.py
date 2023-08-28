from discord import SelectOption, Embed, ButtonStyle
from discord.ui import Select, Button, View

from asyncio import create_task

from Gameplay.Panel import Panel

from WarningMessage import Warning_Message


class WorkPanel(Panel):
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalData, ViewFrame, EmbedFrame):
        if GivenInteraction.user.id == Context.author.id:
            super().__init__(Context, Player, GlobalData)
            self.ViewFrame = ViewFrame
            self.EmbedFrame = EmbedFrame
            self.PlayerPlayPanel = PlayerPlayPanel
            create_task(self.Construct_Panel(GivenInteraction))
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))

    async def Construct_Panel(self, GivenInteraction):
        self.Clear()
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Work Panel", 
                                description=f"aka {self.Player.Profile['Username']}")

        self.WorkSelectionOptions = []
        self.WorkSelection = Select(placeholder="What work would you like to do?", 
                                    options=self.WorkSelectionOptions,
                                    custom_id="Work Selection")
        self.WorkSelection.callback = self.Load_Selection
        self.ViewFrame.add_item(self.WorkSelection)

        if len(self.Player.Jobs) >= 1:
            for JobName, JobObject in self.Player.Jobs.items():
                self.WorkSelectionOptions.append(SelectOption(label=JobName, 
                                                              description=JobObject.Description))
        else:
                self.EmbedFrame.add_field(name="You have no job.", value="You should probably go get one.")

        self.PlayPanelReturnButton = Button(label="Return to Play Panel",
                                            style=ButtonStyle.red,
                                            row=4)
        
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.ViewFrame.add_item(self.PlayPanelReturnButton)
            
        await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)

    async def Load_Selection(self, WorkSelectionInteraction):
        if WorkSelectionInteraction.user.id == self.Context.author.id:
            self.WorkSelection = self.Player.Jobs[WorkSelectionInteraction.data["values"][0]]
            self.WorkSelection.placeholder = WorkSelectionInteraction.data["values"][0]
            WorkButton = Button(label=self.WorkSelection.Name, custom_id="Work Button")
            WorkButton.callback = self.Work
            if WorkButton not in self.ViewFrame.children:
                self.ViewFrame.add_item(WorkButton)
        else:
            create_task(Warning_Message(self.GlobalData, self.Context.author,  WorkSelectionInteraction.user))

        await WorkSelectionInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)

    #### I'm updating the players inventory data in the database for reloading

    async def Work(self, ButtonInteraction):
        if ButtonInteraction.user.id == self.Context.author.id:
            Result = await self.WorkSelection.Harvest(self.Player)
            self.EmbedFrame.clear_fields()
            self.Player.Profile["Hunger"] += 5
            self.Player.Profile["Thirst"] += 5
            self.Player.Profile["Thirst"] += 0.2
            Cursor = self.GlobalData.Database.Generate_Cursor()
            if self.WorkSelection.OutputItem in self.Player.Inventory.keys():
                self.Player.Inventory[self.WorkSelection.OutputItem] += Result[1]
                CurrentInventory = Cursor.execute("SELECT Inventory FROM Players").fetchall()
                Cursor.execute("REPLACE INTO Players(Inventory) ()")
            else:
                self.Player.Inventory.update({self.WorkSelection.OutputItem:Result[0]})
            self.EmbedFrame.insert_field_at(0, name="Successful Harvest", value=Result[1])
            await ButtonInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)
            self.GlobalData.Logger.info(f"{self.Player.Profile['Username']} successfully harvested from {self.WorkSelection.Name} {Result[1]} {self.WorkSelection.OutputItem}")
        else:
            create_task(Warning_Message(self.GlobalData, self.Context.author,  ButtonInteraction.user))