from discord import Embed, ButtonStyle
from discord.ui import View, Button, Modal, TextInput
from asyncio import create_task

class ProfilePanel:
    def __init__(self, Context, Player, GivenInteraction, PlayerPlayPanel, GlobalData):
        self.Context = Context
        self.Player = Player
        self.GivenInteraction = GivenInteraction
        self.GlobalData = GlobalData
        self.PlayerPlayPanel = PlayerPlayPanel
        create_task(self.Construct_Panel())

    async def Construct_Panel(self):
        self.BaseViewFrame = View(timeout=144000)
        self.EmbedFrame = Embed(title=f"{self.Player.Profile['Nickname']}'s Profile Panel", description=f"aka {self.Player.Profile['Username']}")

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
        self.PlayPanelReturnButton = Button(label="Return to Play Panel", style=ButtonStyle.red, row=4)

        self.ChangeNicknameButton.callback = self.Get_Nickname
        self.PlayPanelReturnButton.callback = self.PlayerPlayPanel.Reset

        self.BaseViewFrame.add_item(self.PlayPanelReturnButton)
        self.BaseViewFrame.add_item(self.ChangeNicknameButton)

        await self.GivenInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)

    async def Get_Nickname(self, ButtonInteraction):
        ChangeNicknameModal = Modal(title="Set Nickname")
        ChangeNicknameInput = TextInput(label="Please enter a new nickname")
        ChangeNicknameModal.on_submit = self.Change_Nickname
        ChangeNicknameModal.add_item(ChangeNicknameInput)
        await ButtonInteraction.response.send_modal(ChangeNicknameModal)

    async def Change_Nickname(self, ModalInteraction):
        self.EmbedFrame.clear_fields()
        Nickname = ModalInteraction.data['components'][0]['components'][0]['value']
        self.EmbedFrame.add_field(name="You changed your nickname.", value=f"Your nickname was changed from {self.Player.Profile['Nickname']} to {Nickname}")
        self.Player.Profile["Nickname"] = Nickname
        self.EmbedFrame.title = f"{self.Player.Profile['Nickname']}'s Profile Panel"
        Cursor = self.GlobalData.LeviDatabase.Generate_Cursor()
        Cursor.execute(f"UPDATE Players SET Nickname = ? WHERE UUID=?", (Nickname, self.Player.Profile['UUID']))
        self.GlobalData.LeviDatabase.TWDCONNECTION.commit()
        Cursor.close()
        await ModalInteraction.response.edit_message(embed=self.EmbedFrame, view=self.BaseViewFrame)