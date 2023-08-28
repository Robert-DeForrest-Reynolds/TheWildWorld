from discord import Embed, ButtonStyle
from discord.ui import View, Button, Modal, TextInput

from asyncio import create_task

from Gameplay.Panel import Panel
from Gameplay.ProfilePanel.InventoryPanel import InventoryPanel

from WarningMessage import Warning_Message

class ProfilePanel(Panel):
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
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Profile Panel",
                                description=f"aka {self.Player.Profile['Username']}")

        fields = ["Health", "Hunger", "Thirst", "Sanity", "Morale", "Age"]
        self.ProfileInfo = ""
        for Pair in self.Player.Profile.items():
            if Pair[0] in fields:
                if Pair[0] == 'Wallet':
                    self.ProfileInfo +=f"**{Pair[0]}** ~ ${format(int(Pair[1]), ',')}\n"
                elif type(Pair[1]) == int:
                    self.ProfileInfo +=f"**{Pair[0]}** ~ {format(int(Pair[1]), ',')}\n"
                else:
                    self.ProfileInfo +=f"**{Pair[0]}** ~ {Pair[1]}\n"

        self.EmbedFrame.add_field(name="Stats", value=self.ProfileInfo)

        self.ChangeNicknameButton = Button(label="Change Nickname", style=ButtonStyle.blurple, row=3)
        self.InventoryButton = Button(label="Inventory", style=ButtonStyle.blurple, row=3)
        self.PlayPanelReturnButton = Button(label="Return to Play Panel", style=ButtonStyle.red, row=4)

        self.ChangeNicknameButton.callback = self.Get_Nickname
        self.InventoryButton.callback = self.Construct_Inventory_Panel
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.ViewFrame.add_item(self.ChangeNicknameButton)
        self.ViewFrame.add_item(self.InventoryButton)
        self.ViewFrame.add_item(self.PlayPanelReturnButton)

        await GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)

    async def Get_Nickname(self, ButtonInteraction):
        if ButtonInteraction.user.id == self.Context.author.id:
            ChangeNicknameModal = Modal(title="Set Nickname")
            ChangeNicknameInput = TextInput(label="Please enter a new nickname")
            ChangeNicknameModal.on_submit = self.Change_Nickname
            ChangeNicknameModal.add_item(ChangeNicknameInput)
            await ButtonInteraction.response.send_modal(ChangeNicknameModal)
        else:
            create_task(Warning_Message(self.GlobalData, self.Context.author,  ButtonInteraction.user))

    async def Change_Nickname(self, ModalInteraction):
        if ModalInteraction.user.id == self.Context.author.id:
            self.EmbedFrame.clear_fields()
            Nickname = ModalInteraction.data['components'][0]['components'][0]['value']
            self.EmbedFrame.add_field(name="You changed your nickname.", value=f"Your nickname was changed from {self.Player.Profile['Nickname']} to {Nickname}")
            self.Player.Profile["Nickname"] = Nickname
            self.EmbedFrame.title = f"{self.Player.Profile['Nickname']}'s Profile Panel"
            Cursor = self.GlobalData.Database.Generate_Cursor()
            Cursor.execute(f"UPDATE Players SET Nickname = ? WHERE UUID=?", (Nickname, self.Player.Profile['UUID']))
            self.GlobalData.Database.TWDCONNECTION.commit()
            Cursor.close()
            await ModalInteraction.response.edit_message(embed=self.EmbedFrame, view=self.ViewFrame)
        else:
            create_task(Warning_Message(self.GlobalData, self.Context.author,  ModalInteraction.user))

    async def Construct_Inventory_Panel(self, ButtonInteraction):
        InventoryPanel(self.Context,
                       self.Player,
                       ButtonInteraction,
                       self,
                       self.GlobalData,
                       self.ViewFrame,
                       self.EmbedFrame)