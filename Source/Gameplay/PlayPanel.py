from discord import Embed, SelectOption
from discord.ui import View, Select

from asyncio import create_task

from Gameplay.Panel import Panel
from Gameplay.WorkPanel import WorkPanel
from Gameplay.ProfilePanel import ProfilePanel
from Gameplay.PetsPanel import PetsPanel
from Gameplay.MarketPanel import MarketPanel
from Gameplay.HoldPanel import HoldPanel
from Gameplay.OfficePanel import OfficePanel
from Gameplay.StocksPanel import StocksPanel
from Gameplay.HouseholdPanel import HouseholdPanel

from WarningMessage import Warning_Message

class PlayPanel(Panel):
    def __init__(self, Context, Player, GlobalData):
        GivenInteraction = None
        super().__init__(Context, Player, GlobalData)
        create_task(self.Construct_Panel(GivenInteraction))

    async def Construct_Panel(self, GivenInteraction):
        await self.Cleanup()
        try:
            await self.Context.message.delete()
        except:
            print("poof")
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Main Panel",
                                description=f"aka {self.Player.Profile['Username']}")
        
        self.SelectionOptions = [SelectOption(label="Profile",description="See Character Stats & More"),
                                 SelectOption(label="Work",description="Get to work!"),
                                 SelectOption(label="Household",description="Take care of your household; your home, family, personal assets & more."),
                                 SelectOption(label="Pets",description="Take care of some creatures. Some cute, some not."),
                                 SelectOption(label="Market",description="Trade things with other players."),
                                 SelectOption(label="Office",description="Manage your businesses."),
                                 SelectOption(label="Stocks",description="Invest in the public stocks"),
                                 SelectOption(label="The Hold",description="Interact with The Hold, TWW's official Government.")
        ]
        
        self.Selection = Select(placeholder="Panel Selection",options=self.SelectionOptions)
        self.Selection.callback = lambda SelectInteraction: create_task(self.Create_Panel(SelectInteraction.data["values"][0], SelectInteraction))
        
        self.BaseViewFrame.add_item(self.Selection)

        if GivenInteraction == None:
            self.PanelMessage = await self.Context.send(embed=self.EmbedFrame, view=self.BaseViewFrame)
        else:
            self.PanelMessage = await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)

    async def Create_Panel(self, PanelSelection, SelectInteraction):
        if SelectInteraction.user.id == self.Context.author.id:
            if PanelSelection == "Profile":
                ProfilePanel(self.Context,
                            self.Player,
                            SelectInteraction,
                            self,
                            self.GlobalData)
            if PanelSelection == "Work":
                WorkPanel(self.Context,
                        self.Player,
                        SelectInteraction,
                        self,
                        self.GlobalData)
            if PanelSelection == "Pets":
                PetsPanel(self.Context,
                        self.Player,
                        SelectInteraction,
                        self,
                        self.GlobalData)
            if PanelSelection == "Market":
                MarketPanel(self.Context,
                            self.Player,
                            SelectInteraction,
                            self,
                            self.GlobalData)
            if PanelSelection == "Office":
                OfficePanel(self.Context,
                            self.Player,
                            SelectInteraction,
                            self,
                            self.GlobalData)
            if PanelSelection == "Stocks":
                StocksPanel(self.Context,
                            self.Player,
                            SelectInteraction,
                            self,
                            self.GlobalData)
            if PanelSelection == "The Hold":
                HoldPanel(self.Context,
                        self.Player,
                        SelectInteraction,
                        self,
                        self.GlobalData)
            if PanelSelection == "Household":
                HouseholdPanel(self.Context,
                            self.Player,
                            SelectInteraction,
                            self,
                            self.GlobalData)
        else:
            create_task(Warning_Message(self.GlobalData, self.Context.author,  SelectInteraction.user))