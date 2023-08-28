from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select

from asyncio import create_task

from Gameplay.Panel import Panel

from Jobs.ChopOakTrees import ChopOakTrees
from Jobs.SalmonFishing import SalmonFishing
from Jobs.MineCoal import MineCoal
from Jobs.HarvestApples import HarvestApples
from Jobs.WaterPurifying import WaterPurifying
from Jobs.HarvestWheat import HarvestWheat

from Tools.JobsSelector import JobsSelector

from WarningMessage import Warning_Message

class JobsBoardPanel(Panel):
    def __init__(self, Context, Player, GivenInteraction, HoldPanel, GlobalData, ViewFrame, EmbedFrame):
        if GivenInteraction.user.id == Context.author.id:
            super().__init__(Context, Player, GlobalData)
            self.ViewFrame = ViewFrame
            self.EmbedFrame = EmbedFrame
            self.HoldPanel = HoldPanel
            create_task(self.Construct_Panel(GivenInteraction))
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))

    async def Construct_Panel(self, GivenInteraction):
        self.Clear()
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Job Board Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        PsuedoJobs = {
            "Chop Oak Trees":ChopOakTrees(),
            "Salmon Fishing":SalmonFishing(),
            "Mine Coal":MineCoal(),
            "Harvest Apples":HarvestApples(),
            "Water Purifying":WaterPurifying(),
            "Harvest Wheat":HarvestWheat(),
        }

        for Job in PsuedoJobs.values():
            if Job.Name in self.Player.Jobs.keys():
                self.EmbedFrame.add_field(name=f"{Job.Name} (OBTAINED)", value=Job.Description, inline=False)
            else:
                self.EmbedFrame.add_field(name=Job.Name, value=Job.Description, inline=False)

        self.SelectionOptions = []
        for JobName, Job in PsuedoJobs.items():
            if JobName in self.Player.Jobs.keys():
                self.SelectionOptions.append(SelectOption(label=f"{Job.Name} (OBTAINED)", description=f"{Job.Output} from level 1") )
            else:
                self.SelectionOptions.append(SelectOption(label=Job.Name, description=f"{Job.Output} from level 1") )
        
        self.Selection = Select(placeholder="Apply for Job",
                                options=self.SelectionOptions)


        self.HoldPanelReturnButton = Button(label="Return to Hold Panel",
                                            style=ButtonStyle.red,
                                            row=4)

        self.Selection.callback = self.Give_Job
        self.HoldPanelReturnButton.callback = self.HoldPanel.Reset

        self.ViewFrame.add_item(self.Selection)
        self.ViewFrame.add_item(self.HoldPanelReturnButton)

        await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)

    async def Give_Job(self, SelectInteraction):
        if SelectInteraction.user.id == self.Context.author.id:
            if "OBTAINED" not in SelectInteraction.data['values'][0]:
                self.SelectedJob = SelectInteraction.data['values'][0]
                Job = JobsSelector[self.SelectedJob]()
                self.Player.Jobs.update({self.SelectedJob:Job})
                print(self.Player.Jobs)
                Cursor = self.GlobalData.Database.Generate_Cursor()
                Cursor.execute("INSERT INTO Jobs(JobUUID, OwnerUUID, Name, TerminationDate) VALUES(?, ?, ?, ?)", (Job.UUID, self.Player.Profile["UUID"], Job.Name, Job.TerminationDate))
                self.GlobalData.Database.TWDCONNECTION.commit()
                await self.Reset(SelectInteraction)
            else:
                self.Reset()
        else:
            create_task(Warning_Message(self.GlobalData, self.Context.author,  SelectInteraction.user))

        