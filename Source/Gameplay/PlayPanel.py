from discord import Embed, SelectOption
from discord.ui import View, Select

from asyncio import create_task

from Gameplay.Panel import Panel
from Gameplay.WorkPanel.WorkPanel import WorkPanel
from Gameplay.ProfilePanel.ProfilePanel import ProfilePanel
from Gameplay.CreaturePanel.CreaturePanel import CreaturePanel
from Gameplay.MarketPanel.MarketPanel import MarketPanel
from Gameplay.VERIDIANPanel.VERIDIANPanel import VERIDIANPanel
from Gameplay.HomePanel.HomePanel import HomePanel

from WarningMessage import Warning_Message

class PlayPanel(Panel):
    def __init__(self, Context, Player, GlobalData):
        GivenInteraction = None
        self.ViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed()
        self.ViewFrame.on_timeout = self.TimeoutDelete
        self.Panels = {}
        super().__init__(Context, Player, GlobalData)
        create_task(self.Construct_Panel(GivenInteraction))

    async def Construct_Panel(self, GivenInteraction):
        self.Clear()
        try:
            await self.Context.message.delete()
        except:
            self.GlobalData.Logger.info("Player message already deleted")
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Main Panel",
                                description=f"aka {self.Player.Profile['Username']}")
        
        self.SelectionOptions = [SelectOption(label="Profile",
                                              description="See Character Stats & More"),
                                 SelectOption(label="Home",
                                              description="Go home, care for your family, personal assets & more."),
                                 SelectOption(label="Work",
                                              description="Get to work!"),
                                 SelectOption(label="Creatures",
                                              description="Take care of some creatures. Some cute, some not."),
                                 SelectOption(label="Market",
                                              description="Trade things with other players."),
                                 SelectOption(label="The VERIDIAN",
                                              description="Interact with The VERIDIAN, TWW's official Government.")
        ]
        
        self.Selection = Select(placeholder="Panel Selection",options=self.SelectionOptions)
        self.Selection.callback = lambda SelectInteraction: create_task(self.Create_Panel(SelectInteraction.data["values"][0], SelectInteraction))
        
        self.ViewFrame.add_item(self.Selection)

        if GivenInteraction == None:
            self.PanelMessage = await self.Context.send(embed=self.EmbedFrame, view=self.ViewFrame)
        else:
            self.PanelMessage = GivenInteraction.message
            await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)

    async def Create_Panel(self, PanelSelection, SelectInteraction):
        if SelectInteraction.user.id == self.Context.author.id:
            self.ViewFrame.timeout = 144000
            if PanelSelection == "Profile":
                self.Panels.update({"Profile Panel":ProfilePanel(self.Context,
                                                                 self.Player,
                                                                 SelectInteraction,
                                                                 self,
                                                                 self.GlobalData,
                                                                 self.ViewFrame,
                                                                 self.EmbedFrame)})
            if PanelSelection == "Work":
                self.Panels.update({"Work Panel":WorkPanel(self.Context,
                                                           self.Player,
                                                           SelectInteraction,
                                                           self,
                                                           self.GlobalData,
                                                           self.ViewFrame,
                                                           self.EmbedFrame)})
            if PanelSelection == "Creatures":
                self.Panels.update({"Creature Panel":CreaturePanel(self.Context,
                                                                   self.Player,
                                                                   SelectInteraction,
                                                                   self,
                                                                   self.GlobalData,
                                                                   self.ViewFrame,
                                                                   self.EmbedFrame)})
            if PanelSelection == "Market":
                self.Panels.update({"Market Panel":MarketPanel(self.Context,
                                                               self.Player,
                                                               SelectInteraction,
                                                               self,
                                                               self.GlobalData,
                                                               self.ViewFrame,
                                                               self.EmbedFrame)})
            if PanelSelection == "The VERIDIAN":
                self.Panels.update({"VERIDIAN Panel":VERIDIANPanel(self.Context,
                                                                   self.Player,
                                                                   SelectInteraction,
                                                                   self,
                                                                   self.GlobalData,
                                                                   self.ViewFrame,
                                                                   self.EmbedFrame)})
            if PanelSelection == "Home":
                self.Panels.update({"Home Panel":HomePanel(self.Context,
                                                           self.Player,
                                                           SelectInteraction,
                                                           self,
                                                           self.GlobalData,
                                                           self.ViewFrame,
                                                           self.EmbedFrame)})
        else:
            create_task(Warning_Message(self.GlobalData, self.Context.author,  SelectInteraction.user))