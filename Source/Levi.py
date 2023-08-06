from discord import Intents
from discord.ext import commands
from Gameplay.PlayPanel import PlayPanel
from Player import Player
from TWD import TWD
from GD import GD
from CreateProfile import CreateProfile

from sys import argv

GlobalData = GD()

GlobalData.Key = argv[1]
GlobalData.KeyType = argv[2]

intents = Intents.all()
intents.members = True
Levi = commands.Bot(command_prefix=['T', 't'], intents=intents)

if GlobalData.KeyType in ["lani", "robert"]:
    if GlobalData.KeyType == "lani":
        Levi.command_prefix = "-"
    if GlobalData.KeyType == "robert":
        Levi.command_prefix = ">"
    GlobalData.Debug = True
    GlobalData.Unstable = False
elif GlobalData.KeyType == "unstable":
    GlobalData.Debug = True
    GlobalData.Unstable = True
elif GlobalData.KeyType == "official":
    Levi.command_prefix = ["T", "t"]

print(f"Command Prefix: {Levi.command_prefix}")


@Levi.event
async def on_member_join(Member):
    await CreateProfile(Member, GlobalData)


@Levi.event
async def on_ready():
    if GlobalData.Debug == True:
        for Guild in Levi.guilds:
            GlobalData.Guilds.append(Guild)
        for Member in GlobalData.Guilds[0].members:
            GlobalData.FoundMembers.update({Member.name: Player(Member)})
        GlobalData.LeviDatabase = TWD(GlobalData)
    if GlobalData.Unstable == True:
        for Guild in Levi.guilds:
            GlobalData.Guilds.append(Guild)
        for Member in GlobalData.Guilds[0].members:
            GlobalData.FoundMembers.update({Member.name: Player(Member)})
        GlobalData.LeviDatabase = TWD(GlobalData)
    if GlobalData.Debug == False and GlobalData.Unstable == False:
        for Guild in Levi.guilds:
            GlobalData.Guilds.append(Guild)
        for Member in GlobalData.Guilds[0].members:
            GlobalData.FoundMembers.update({Member.name: Player(Member)})
        GlobalData.LeviDatabase = TWD(GlobalData)

    GlobalData.Players = GlobalData.LeviDatabase.Load_Players(GlobalData)
    print(GlobalData.Players)

    GlobalData.LeviDatabase.Save_Global_Data(GlobalData)


@Levi.command(aliases=["WW", "ww", "wW", "Ww"])
async def Play_Command(Context):
    if Context.author.id in list(GlobalData.Players.keys()):
        if GlobalData.Players[Context.author.id].PanelOn == False:
            GlobalData.Logger.info(f"{Context.author} called for a panel")
            GlobalData.PlayerPanels.update({Context.author.id:PlayPanel(Context, GlobalData)})
            GlobalData.Players[Context.author.id].PanelOn = True
        else:
            await GlobalData.PlayerPanels[Context.author.id].Delete()
            # del GlobalData.PlayerPanels[Context.author.id]
            GlobalData.PlayerPanels.update({Context.author.id:PlayPanel(Context, GlobalData)})
            GlobalData.Players[Context.author.id].PanelOn = True
    else:
        GlobalData.Logger.info(f"{Context.author} called for a panel, but broke something. Fuckin' hell.")
        await Context.send("You do not have a profile yet. Stop breaking stuff. How did this even happen?")


@Levi.command("create_profile")
@commands.has_permissions(administrator=True)
async def Admin_Create_Profile(Context):
    Member = GlobalData.FoundMembers[Context.author.name].Profile["Member Object"]
    await CreateProfile(Member, GlobalData, GlobalData.Logger)


@Levi.command("delete_profile")
@commands.has_permissions(administrator=True)
async def Delete_Profile(Context, GivenUsername):
    Cursor = GlobalData.LeviDatabase.Generate_Cursor()
    Cursor.execute(f"DELETE FROM Players WHERE Username='{GivenUsername}'")
    GlobalData.LeviDatabase.TWDCONNECTION.commit()
    Cursor.close()
    GlobalData.Logger.info(f"Attempted to delete {GivenUsername}'s profile")
    if GivenUsername in GlobalData.LeviDatabase.Cursor.execute(f"SELECT Username FROM Players WHERE Username='{GivenUsername}'").fetchall()[0]:
        GlobalData.Logger.info(f"Successfully deleted {GivenUsername}'s profile")
    else:
        GlobalData.Logger.info(f"Successfully deleted {GivenUsername}'s profile")


print(f"Running bot as {GlobalData.KeyType}")
GlobalData.Logger.info(f"Running bot as {GlobalData.KeyType}")

Levi.run(GlobalData.Key)