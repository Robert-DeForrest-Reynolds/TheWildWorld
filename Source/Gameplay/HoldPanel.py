from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select

from asyncio import create_task

from Gameplay.Panel import Panel
from Gameplay.JobsBoardPanel import JobsBoardPanel

from WarningMessage import Warning_Message

class HoldPanel(Panel):
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalData):
        if GivenInteraction.user.id == Context.author.id:
            super().__init__(Context, Player, GlobalData)
            self.PlayerPlayPanel = PlayerPlayPanel
            create_task(self.Construct_Panel(GivenInteraction))
        else:
            create_task(Warning_Message(self.GlobalData, Context.author,  GivenInteraction.user))

    async def Construct_Panel(self, GivenInteraction):
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Hold Panel",
                                description=f"aka {self.Player.Profile['Username']}")
    
        self.SelectionOptions = [SelectOption(label="Job Board",
                                              description="Obtain Jobs! New jobs every week (RLT)!"),
        ]

        self.Selection = Select(placeholder="What can the Hold do for you?",
                                options=self.SelectionOptions)
        
        self.PlayPanelReturnButton = Button(label="Return to Play Panel",
                                            style=ButtonStyle.red,
                                            row=4)

        self.Selection.callback = self.Create_Panel
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.BaseViewFrame.add_item(self.Selection)
        self.BaseViewFrame.add_item(self.PlayPanelReturnButton)

        await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)

    async def Create_Panel(self, SelectInteraction):
        if SelectInteraction.user.id == self.Context.author.id:
            self.SelectedPanel = SelectInteraction.data['values'][0]
            
            if self.SelectedPanel == "Job Board":
                JobsBoardPanel(self.Context,
                               self.Player,
                               SelectInteraction,
                               self,
                               self.GlobalData)
        