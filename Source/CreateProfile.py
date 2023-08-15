from discord.ui import View, Button, Modal, TextInput
from discord import ButtonStyle
from PlayerObject import PlayerObject
from Jobs.HarvestApples import HarvestApples
from Jobs.ChopOakTrees import ChopOakTrees
from Jobs.MineCoal import MineCoal

JobsSelector = {"Harvest Apples": HarvestApples,
                "Chop Trees": ChopOakTrees,
                "Mine Coal": MineCoal}

LeviIntroduction = ("Hello, my name is Levi Kiln. I'm here to introduce to you to the Wild World. "+
                    "You'll first land within Harna, where the main camp The Hold has developed. "+
                    "I'm going to let you choose from three of the jobs The Hold provides people with. "+
                    "Harvesting apples, chopping trees, or mining. "+
                    "Which would you like to do?")

LeviPassword = ("One more thing! I'll need you to make a password now for your account."+
                "This is in case of data-transfer, and a couple other reasons.")

async def CreateProfile(Member, GlobalData):
    async def Set_Password(ModalInteraction, SelectedWork):
        Password = ModalInteraction.data['components'][0]['components'][0]['value']
        NewPlayer.Password = Password
        ResponseDictionary = {"Harvest Apples": "I can't wait to taste some of those apples!",
                              "Chop Trees": "You should sell some of that lumber to Harold!",
                              "Mine Coal": "Mining coal? Man, I hope your back is strong!"}
        GlobalData.Logger.info(f"Created a profile.\nName:{NewPlayer.Profile['Username']}, SelectedWork:{SelectedWork}, Password:{Password}")
        Cursor = GlobalData.Database.Generate_Cursor()
        Cursor.execute(f"INSERT OR IGNORE INTO Players(UUID, Username, Nickname, Password, ProfileCreationDate) VALUES(?, ?, ?, ?, ?)",
                                               (NewPlayer.Profile["UUID"], NewPlayer.Profile["Username"], NewPlayer.Profile["Nickname"], NewPlayer.Password, NewPlayer.ProfileCreationDate))
        GlobalData.Database.TWDCONNECTION.commit()
        Cursor.close()
        await ModalInteraction.response.send_message(f"Alright then! You've set your password to '{Password}'. {ResponseDictionary[SelectedWork]} I wish you the best of luck on your adventures! We'll talk more soon I'm sure.")
    async def Select_Work(ButtonInteraction):
        SelectedWork = ButtonInteraction.data["custom_id"]
        NewPlayer.Jobs.update({SelectedWork: JobsSelector[SelectedWork]()})
        PasswordModal = Modal(title="Set Password")
        PasswordInput = TextInput(label="Please enter a password")
        PasswordModal.on_submit = lambda ModalInteraction: Set_Password(ModalInteraction, SelectedWork)
        PasswordModal.add_item(PasswordInput)
        await ButtonInteraction.response.send_modal(PasswordModal)

    ViewFrame = View()
    AppleButton = Button(label="Harvest Apples", style=ButtonStyle.blurple, custom_id="Harvest Apples")
    ChoppingButton = Button(label="Chop Trees", style=ButtonStyle.blurple, custom_id="Chop Trees")
    MiningButton = Button(label="Mine Coal", style=ButtonStyle.blurple, custom_id="Mine Coal")
    ViewFrame.add_item(AppleButton)
    ViewFrame.add_item(ChoppingButton)
    ViewFrame.add_item(MiningButton)
    AppleButton.callback = Select_Work
    ChoppingButton.callback = Select_Work
    MiningButton.callback = Select_Work
    NewPlayer = PlayerObject(Member)
    GlobalData.Members[NewPlayer.Profile["UUID"]] = NewPlayer
    GlobalData.Players.update({NewPlayer.Profile["UUID"]:NewPlayer})
    await Member.send(LeviIntroduction, view=ViewFrame)
