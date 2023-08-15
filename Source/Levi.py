from discord import Intents, RateLimited
from discord.ext import commands
from Gameplay.PlayPanel import PlayPanel
from TWD import TWD
from GD import GD
from CreateProfile import CreateProfile
from WorldSimulation import WorldSimulation

from sys import argv

GlobalData = GD()

GlobalData.Key = argv[1]
GlobalData.KeyType = argv[2]

intents = Intents.all()
intents.members = True
Levi = commands.Bot(command_prefix=['.'], intents=intents)

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
    Levi.command_prefix = ["."]

print(f"Command Prefix: {Levi.command_prefix}")

@Levi.event
async def on_member_join(Member):
    await CreateProfile(Member, GlobalData)


@Levi.event
async def on_ready():
    if len(Levi.guilds) == 1:
        GlobalData.Guild = Levi.guilds[0]
    else:
        print("Why the fuck did I detect two guilds? Stop fucking around.")
    GlobalData.Members = {Member.name: Member for Member in GlobalData.Guild.members}
    GlobalData.Channels = {Channel.name:Channel for Channel in GlobalData.Guild.channels}

    GlobalData.Database = TWD(GlobalData)

    GlobalData.Players = GlobalData.Database.Load_Players(GlobalData)

    GlobalData.Database.Save_Global_Data(GlobalData)

    WS = WorldSimulation(GlobalData)


@Levi.command(aliases=["TWW", "tWW", "Tww", "tww", "TwW", "twW", "TWw", "tWw"])
async def Play_Command(Context):
    if Context.author.id in list(GlobalData.Players.keys()):
        if GlobalData.Players[Context.author.id].PanelOn == False:
            GlobalData.Logger.info(f"{Context.author} called for a panel")
            GlobalData.PlayerPanels.update({Context.author.id:PlayPanel(Context, GlobalData)})
            GlobalData.Players[Context.author.id].PanelOn = True
        else:
            await GlobalData.PlayerPanels[Context.author.id].Delete()
            del GlobalData.PlayerPanels[Context.author.id]
            GlobalData.PlayerPanels.update({Context.author.id:PlayPanel(Context, GlobalData)})
            GlobalData.Players[Context.author.id].PanelOn = True
    else:
        GlobalData.Logger.info(f"{Context.author} called for a panel, but broke something. Fuckin' hell.")
        await Context.send("You do not have a profile yet. Stop breaking stuff. How did this even happen?")
        await Context.message.delete()


@Levi.command(aliases=["Cleanup", "cleanup"])
@commands.has_permissions(administrator=True)
async def Stop_Bot_Properly(Context):
    GlobalData.Logger.info("Started cleaning up")
    async for Message in GlobalData.Channels['town-hall'].history(limit=None):
        if Message.author.bot == True:
            try:
                await Message.delete()
            except RateLimited:
                continue
        if Message.content.startswith(Levi.command_prefix):
            try:
                await Message.delete()
            except RateLimited:
                continue
    for PlayerID, Panel in GlobalData.PlayerPanels.items():
        await Panel.Delete()
        del GlobalData.PlayerPanels[PlayerID]
    GlobalData.Logger.info("Finished cleaning up")


@Levi.command("create_profile")
@commands.has_permissions(administrator=True)
async def Admin_Create_Profile(Context):
    Member = GlobalData.Members[Context.author.name]
    await CreateProfile(Member, GlobalData)


@Levi.command("delete_profile")
@commands.has_permissions(administrator=True)
async def Delete_Profile(Context, GivenUsername):
    Cursor = GlobalData.Database.Generate_Cursor()
    Cursor.execute(f"DELETE FROM Players WHERE Username='{GivenUsername}'")
    GlobalData.Database.TWDCONNECTION.commit()
    Cursor.close()
    GlobalData.Logger.info(f"Attempted to delete {GivenUsername}'s profile")
    if GivenUsername in GlobalData.Database.Cursor.execute(f"SELECT Username FROM Players WHERE Username='{GivenUsername}'").fetchall()[0]:
        GlobalData.Logger.info(f"Successfully deleted {GivenUsername}'s profile")
    else:
        GlobalData.Logger.info(f"Successfully deleted {GivenUsername}'s profile")


print(f"Running bot as {GlobalData.KeyType}")
GlobalData.Logger.info(f"Running bot as {GlobalData.KeyType}")

Levi.run(GlobalData.Key)