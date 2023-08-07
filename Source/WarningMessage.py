async def Warning_Message(GlobalData, ProperUser, WrongfulUser):
    GlobalData.Logger.info(f"{WrongfulUser} attempted to use {ProperUser}'s panel.")
    await WrongfulUser.send("Please stop messing with other peoples panels. You have been warned.")