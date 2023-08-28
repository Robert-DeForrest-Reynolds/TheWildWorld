from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Modal, TextInput, Select

from asyncio import create_task

from Gameplay.Panel import Panel

from WarningMessage import Warning_Message

class InventoryPanel(Panel):
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
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Inventory Panel",
                                description=f"aka {self.Player.Profile['Username']}")

        self.WarehouseSelectOptions = []
        for WarehouseCount in range(self.Player.WarehouseCount):
            self.WarehouseSelectOptions.append(SelectOption(label=f"Warehouse {WarehouseCount}", description=""))

        self.InventorySelectOptions = []
        self.InventoryIndex = 0
        for _ in range(25):
            self.InventoryIndex += 1
            for Item, Quantity in self.Player.Inventory:
                self.InventorySelectOptions.append(SelectOption(label=Item, description=Quantity))
        print(self.InventoryIndex)

        self.WarehouseSelection = Select(placeholder="Warehouse 1", options=self.WarehouseSelectOptions)
        self.InventorySelection = Select(placeholder="Inventory", options=self.InventorySelectOptions)

        self.PlayPanelReturnButton = Button(label="Return to Play Panel", style=ButtonStyle.red, row=4)

        self.WarehouseSelection.callback = self.Load_Warehouse
        self.InventorySelection.callback = self.Item_Interaction
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.ViewFrame.add_item(self.WarehouseSelection)
        self.ViewFrame.add_item(self.InventorySelection)
        self.ViewFrame.add_item(self.PlayPanelReturnButton)

        await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)

    async def Load_Warehouse(self, SelectInteraction):
        pass

    async def Item_Interaction(self, SelectInteraction):
        pass