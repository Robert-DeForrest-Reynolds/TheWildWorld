from discord.ui import View, Button
from discord import ButtonStyle
from Player import Player
from Work.GrowApples import GrowApples
from Work.ChopTrees import ChopTrees
from Work.MineCoal import MineCoal

JobsSelector = {"Grow Apples": GrowApples,
                "Chop Trees": ChopTrees,
                "Mine Coal": MineCoal}

LeviIntroduction = ("Hello, my name is Levi Kiln. I'm here to introduce to you to the Wild World. "+
                    "You'll first land within Harna, the main camp The Hold has developed. "+
                    "I'm going to let you choose from three jobs The Hold provides people with. "+
                    "Growing apples, chopping trees, or mining. "+
                    "Which would you like to do?")

async def CreateProfile(Member, GlobalData):
    async def SelectWork(ButtonInteraction):
        SelectedWork = ButtonInteraction.data["custom_id"]
        NewPlayer.Jobs.append(JobsSelector[SelectedWork]())
        ResponseDictionary = {"Grow Apples": "I can't wait to taste some of those apples!",
                              "Chop Trees": "You should sell some of that lumber to Harold!",
                              "Mine Coal": "Mining coal? Man, I hope your back is strong!"}
        await ButtonInteraction.response.send_message(f"Alright then! {ResponseDictionary[SelectedWork]}. I wish you the best of luck on your adventures! We'll talk more soon I'm sure.")

    ViewFrame = View()
    AppleButton = Button(label="Grow Apples", style=ButtonStyle.blurple, custom_id="Grow Apples")
    ChoppingButton = Button(label="Chop Trees", style=ButtonStyle.blurple, custom_id="Chop Trees")
    MiningButton = Button(label="Mine Coal", style=ButtonStyle.blurple, custom_id="Mine Coal")
    ViewFrame.add_item(AppleButton)
    ViewFrame.add_item(ChoppingButton)
    ViewFrame.add_item(MiningButton)
    AppleButton.callback = SelectWork
    ChoppingButton.callback = SelectWork
    MiningButton.callback = SelectWork
    NewPlayer = Player(Member)
    GlobalData.LeviMembers[NewPlayer.Name] = NewPlayer
    await Member.send(LeviIntroduction, view=ViewFrame)